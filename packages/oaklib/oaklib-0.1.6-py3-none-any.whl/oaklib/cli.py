"""
Command Line Interface to OAK
-----------------------------

Executed using "runoak" command
"""
import logging
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, TextIO, Tuple, Any, Type

import click
from linkml_runtime.dumpers import yaml_dumper, json_dumper
from oaklib.datamodels.validation_datamodel import ValidationConfiguration
from oaklib.implementations.bioportal.bioportal_implementation import BioportalImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph.ubergraph_implementation import UbergraphImplementation
from oaklib.interfaces import BasicOntologyInterface, OntologyInterface, ValidatorInterface, SubsetterInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.resource import OntologyResource
from oaklib.types import PRED_CURIE
from oaklib.utilities.apikey_manager import set_apikey_value
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom, \
    load_lexical_index, load_mapping_rules, add_labels_from_uris
from oaklib.utilities.obograph_utils import draw_graph, graph_to_image, default_stylemap_path
import sssom.writers as sssom_writers
from oaklib.datamodels.vocabulary import IS_A, PART_OF, EQUIVALENT_CLASS


@dataclass
class Settings:
    impl: Any = None


settings = Settings()

input_option = click.option(
    "-i",
    "--input",
    help="path to input implementation specification."
)
input_type_option = click.option(
    "-I",
    "--input-type",
    help="Input type."
)
output_option = click.option(
    "-o",
    "--output",
    type=click.File(mode="w"),
    default=sys.stdout,
    help="Output file, e.g. obo file"
)
output_type_option = click.option(
    "-O",
    "--output-type",
    help=f'Desired output type',
)
predicates_option = click.option(
    "-p",
    "--predicates",
    help="A comma-separated list of predicates"
)

def _process_predicates_arg(preds_str: str) -> List[PRED_CURIE]:
    if preds_str is None:
        return None
    inputs = preds_str.split(',')
    preds = [_shorthand_to_pred_curie(p) for p in inputs]
    return preds

def _shorthand_to_pred_curie(shorthand: str) -> PRED_CURIE:
    if shorthand == 'i':
        return IS_A
    elif shorthand == 'p':
        return PART_OF
    elif shorthand == 'e':
        return EQUIVALENT_CLASS
    else:
        return shorthand


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@input_option
def main(verbose: int, quiet: bool, input: str):
    """Run the oaklib Command Line.

    A subcommand must be passed - for example: ancestors, terms, ...

    Most commands require an input ontology to be specified:

        runoak -i <INPUT SPECIFICATION> SUBCOMMAND <SUBCOMMAND OPTIONS AND ARGUMENTS>

    Get help on any command, e.g:

        runoak viz -h
    """
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if quiet:
        logging.basicConfig(level=logging.ERROR)
    resource = OntologyResource()
    resource.slug = input
    impl_class: Type[OntologyInterface]
    # TODO: move to a separate module
    if input:
        if ':' in input:
            toks = input.split(':')
            scheme = toks[0]
            rest = ':'.join(toks[1:])
            if scheme == 'sqlite':
                impl_class = SqlImplementation
                resource.slug = f'sqlite:///{Path(rest).absolute()}'
            elif scheme == 'ubergraph':
                impl_class = UbergraphImplementation
                resource = None
            elif scheme == 'ontobee':
                impl_class = OntobeeImplementation
                resource = None
            elif scheme == 'bioportal':
                impl_class = BioportalImplementation
                resource = None
            elif scheme == 'obolibrary':
                impl_class = ProntoImplementation
                if resource.slug.endswith('.obo'):
                    resource.format = 'obo'
                resource.local = False
                resource.slug = resource.slug.replace('obolibrary:', '')
            else:
                raise ValueError(f'Scheme {scheme} not known')
        else:
            resource.local = True
            impl_class = ProntoImplementation
        logging.info(f'RESOURCE={resource}')
        settings.impl = impl_class(resource)


@main.command()
@click.argument("terms", nargs=-1)
@output_option
def search(terms, output: str):
    """
    Searches ontology for entities that have a label, alias, or other property matching a search term.

    Example:
        runoak -i uberon.obo search limb

    This uses the Pronto implementation to load uberon from disk, and does a basic substring
    search over the labels and synonyms - results are not ranked

    Bioportal:
        runoak -i uberon.obo search limb

    (You need to set your API key first)

    This uses the Bioportal API to search over a broad set of ontologies, returning a ranked list
    ranked by relevance. There may be many results, the results are streamed, do ctrl^C to stop
    """
    impl = settings.impl
    if isinstance(impl, SearchInterface):
        for t in terms:
            for curie_it in chunk(impl.basic_search(t)):
                logging.info('** Next chunk:')
                for curie, label in impl.get_labels_for_curies(curie_it):
                    print(f'{curie} ! {label}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("subset")
@output_option
def list_subset(subset, output: str):
    """
    Shows IDs in a given subset

    Example:
        runoak -i obolibrary:go.obo list-subset goslim_generic

    Example:
        oak -i sqlite:notebooks/input/go.db list-subset goslim_agr
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.curies_by_subset(subset):
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("words", nargs=-1)
@output_option
def annotate(words, output: str):
    """
    Annotate a piece of text using a Named Entity Recognition annotation

    Example:
        runoak -i bioportal: annotate "enlarged nucleus in T-cells from peripheral blood"
    """
    impl = settings.impl
    text = ' '.join(words)
    if isinstance(impl, TextAnnotatorInterface):
        for ann in impl.annotate_text(text):
            print(yaml_dumper.dumps(ann))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option("--view/--no-view",
              default=True,
              show_default=True,
              help="if view is set then open the image after rendering")
@click.option("--down/--no-down",
              default=False,
              show_default=True,
              help="traverse down")
@click.option('-S', '--stylemap',
              help='a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/')
@click.option('-C', '--configure',
              help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `')
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
# TODO: the main output option uses a filelike object
@click.option('-o', '--output',
              help="Path to output file")
#@output_option
def viz(terms, predicates, down, view, stylemap, configure, output_type: str, output: str):
    """
    Visualizing an ancestor graph using obographviz

    Note the implementation must implement :class:`.OboGraphInterface`

    This requires that `obographviz <https://github.com/cmungall/obographviz>`_ is installed.

    Example:

        runoak -i sqlite:cl.db viz CL:4023094

    Example, showing only is-a:

        runoak -i sqlite:cl.db viz CL:4023094 -p i

    Example, showing only is-a and part-of, to include Uberon:

        runoak -i sqlite:cl.db viz CL:4023094 -p i,p

    As above, including develops-from:

        runoak -i sqlite:cl.db viz CL:4023094 -p i,p,RO:0002202
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        if stylemap is None:
            stylemap = default_stylemap_path()
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(impl.multiterm_search(terms))
        if down:
            graph = impl.subgraph(curies, predicates=actual_predicates)
        else:
            graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        logging.info(f'Drawing graph seeded from {curies}')
        if output_type == 'json':
            if output:
                json_dumper.dump(graph, to_file=output)
            else:
                print(json_dumper.dumps(graph))
        elif output_type == 'yaml':
            if output:
                yaml_dumper.dump(graph, to_file=output)
            else:
                print(yaml_dumper.dumps(graph))
        else:
            imgfile = graph_to_image(graph, seeds=curies, stylemap=stylemap, configure=configure, imgfile=output)
            if view:
                subprocess.run(['open', imgfile])
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
def ancestors(terms, predicates, output: str):
    """
    List all ancestors

    Example:

        runoak -i cl.owl ancestors CL:4023094

    Note that ancestors is by default over ALL relationship types

    Constrained to is-a and part-of:

        runoak -i cl.owl ancestors CL:4023094 -p i,BFO:0000050

    Same, on ubergraph:

        runoak -i ubergraph: ancestors CL:4023094 -p i,BFO:0000050

    Search terms can also be used:

        runoak -i cl.owl ancestors 'goblet cell'

    Multiple terms can be passed:

        runoak -i sqlite:go.db ancestors GO:0005773 GO:0005737 -p i,p
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface) and isinstance(impl, SearchInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(impl.multiterm_search(terms))
        logging.info(f'Ancestor seed: {curies}')
        graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        for n in graph.nodes:
            print(f'{n.id} ! {n.label}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
def descendants(terms, predicates, output: str):
    """
    List all descendants of a term

    See examples for 'ancestors' command
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        graph = impl.descendant_graph(list(impl.multiterm_search(terms)), predicates=actual_predicates)
        for n in graph.nodes:
            print(f'{n.id} ! {n.label}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@output_option
def info(terms, output: str):
    """
    Show info on terms

    TODO: currenly this only shows the label

    Example:
        runoak -i cl.owl info CL:4023094
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        curies = list(impl.multiterm_search(terms))
        for curie in curies:
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@output_option
def relationships(terms, output: str):
    """
    Show relationships for terms

    Example:
        runoak -i cl.owl relationships CL:4023094
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        curies = list(impl.multiterm_search(terms))
        for curie in curies:
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
            for pred, fillers in impl.get_outgoing_relationships_by_curie(curie):
                print(f'  PRED: {pred} ! {impl.get_label_by_curie(pred)}')
                for filler in fillers:
                    print(f'    * {filler} ! {impl.get_label_by_curie(filler)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@output_option
def terms(output: str):
    """
    List all terms in the ontology
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.all_entity_curies():
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def axioms(output: str):
    """
    List all axioms

    TODO: this is a placeholder -- will be added when we add funowl
    """
    impl = settings.impl
    #if isinstance(impl, OwlInterface):
    #    for axiom in impl.axioms():
    #        print(f'{axiom}')
    #else:
    #    raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')
    raise NotImplementedError


@main.command()
@click.option('--cutoff',
              default=50,
              show_default=True,
              help="maximum results to report for any (type, predicate) pair")
@output_option
def validate(output: str, cutoff: int):
    """
    Validate an ontology against ontology metadata
    """
    impl = settings.impl
    if isinstance(impl, ValidatorInterface):
        counts = defaultdict(int)
        for result in impl.validate():
            key = (result.type, result.predicate)
            n = counts[key]
            n += 1
            counts[key] = n
            if n % 1000 == 0:
                logging.info(f'Reached {n} results with {key}')
            if n == cutoff:
                print(f'**TRUNCATING RESULTS FOR {key} at {cutoff}')
            elif n < cutoff:
                print(yaml_dumper.dumps(result))
        for k, v in counts.items():
            print(f'{k}:: {v}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option('--cutoff',
              default=50,
              show_default=True,
              help="maximum results to report for any (type, predicate) pair")
@click.option('-s', '--schema',
              help="Path to schema (if you want to override the bundled OMO schema)")
@click.argument("dbs", nargs=-1)
@output_option
def validate_multiple(dbs, output, schema, cutoff: int):
    """
    Validate an ontology against ontology metadata
    """
    writer = StreamingCsvWriter(output)
    config = ValidationConfiguration()
    if schema:
        config.schema_path = schema
    for db in dbs:
        try:
            path = Path(db).absolute()
            print(f'PATH={path}')
            resource = OntologyResource(slug=f'sqlite:///{str(path)}')
            impl = SqlImplementation(resource)
            counts = defaultdict(int)
            for result in impl.validate(configuration=config):
                result.source = f'sqlite:{db}'
                key = (result.type, result.predicate)
                n = counts[key]
                n += 1
                counts[key] = n
                if n % 1000 == 0:
                    logging.info(f'Reached {n} results with {key}')
                if n == cutoff:
                    print(f'**TRUNCATING RESULTS FOR {key} at {cutoff}')
                elif n < cutoff:
                    try:
                        print(yaml_dumper.dumps(result))
                        writer.emit(result)
                    except ValueError as e:
                        logging.error(e)
                        logging.error(f'Could not dump {result} -- bad identifier?')
        except Exception as e:
            logging.error(e)
            logging.error(f'Problem with db')
        for k, v in counts.items():
            print(f'{k}:: {v}')


@main.command()
@output_option
def check_definitions(output: str):
    """
    Check definitions
    """
    impl = settings.impl
    if isinstance(impl, ValidatorInterface):
        for curie in impl.term_curies_without_definitions():
            print(f'NO DEFINITION: {curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')



@main.command()
@click.argument("curies", nargs=-1)
@output_option
def subset(curies, output: str):
    """
    Extracts a subset

    TODO: INCOMPLETE
    """
    impl = settings.impl
    if isinstance(impl, SubsetterInterface):
        subont = impl.extract_subset_ontology(curies)
        print(f'TODO: {subont}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.option('--endpoint',
              '-e')
@click.argument("keyval")
def set_apikey(endpoint, keyval):
    """
    Sets an API key

    Example:
        oak set-apikey -e bioportal MY-KEY-VALUE
    """
    set_apikey_value(endpoint, keyval)


@main.command()
@click.option("--lexical-index-file", "-L",
              help="path to lexical index. This is recreated each time unless --no-recreate is passed")
@click.option("--rules-file", "-R",
              help="path to rules file. Conforms to rules_datamodel.")
@click.option("--add-labels/--no-add-labels",
              default=False,
              show_default=True,
              help="Populate empty labels with URI fragments or CURIE local IDs, for ontologies that use semantic IDs")
@click.option("--recreate/--no-recreate",
              default=True,
              show_default=True,
              help="if true and lexical index is specified, always recreate, otherwise load from index")
@output_option
def lexmatch(output, recreate, rules_file, lexical_index_file, add_labels):
    """
    Generates lexical index and mappings

    See :ref:`.lexical_index_to_sssom`

    Examples:
        lexmatch -i foo.obo -o foo.sssom.tsv

    Outputting intermediate index:
        lexmatch -i foo.obo -L foo.index.yaml -o foo.sssom.tsv

    Using custom rules:
        lexmatch -i foo.obo -R match_rules.yaml -L foo.index.yaml -o foo.sssom.tsv
    """
    impl = settings.impl
    if rules_file:
        ruleset = load_mapping_rules(rules_file)
    else:
        ruleset = None
    if isinstance(impl, BasicOntologyInterface):
        if add_labels:
            add_labels_from_uris(impl)
        if not recreate and Path(lexical_index_file).exists():
            ix = load_lexical_index(lexical_index_file)
        else:
            ix = create_lexical_index(impl)
        if lexical_index_file:
            if recreate:
                save_lexical_index(ix, lexical_index_file)
        msdf = lexical_index_to_sssom(impl, ix, ruleset=ruleset)
        sssom_writers.write_table(msdf, output)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


if __name__ == "__main__":
    main()
