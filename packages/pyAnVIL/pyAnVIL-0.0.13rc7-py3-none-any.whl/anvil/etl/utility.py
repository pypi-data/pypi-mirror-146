import click
import logging
import yaml
import json

from anvil.etl.transform import _consortium_from_workspace
from anvil.etl.transformers.fhir_writer import ensure_data_store_name
from anvil.etl.transformers.normalizer import get_pickled_workspace, fetch_workspace_names

logger = logging.getLogger(__name__)


@click.group(name='utility')
@click.pass_context
def utility(ctx):
    """Utility commands."""
    pass


@utility.command(name='config')
@click.option('--format', type=click.Choice(['json', 'yaml'],case_sensitive=False), default='json', show_default=True)
@click.pass_context
def _config(ctx, format):
    """Print config to stdout."""
    if format == 'yaml':
        print(yaml.dump(ctx.obj['config']))
    else:
        print(json.dumps(ctx.obj['config']))


@utility.command(name='data-stores')
@click.option('--consortium', default=None, help='Filter, only this consortium.')
@click.option('--workspace', default=None, help='Filter, only this workspace.')
@click.pass_context
def _data_stores(ctx, consortium, workspace):
    """Print workspace data-store info to stdout."""
    if not consortium and workspace:
        consortium = _consortium_from_workspace(ctx.obj['config'], workspace)
        workspace_names = [(consortium, workspace)]
    else:
        workspace_names = fetch_workspace_names(ctx.obj['output_path'], requested_consortium_name=consortium, workspace_name=workspace)
    for consortium_name, workspace_name in workspace_names:
        workspace = get_pickled_workspace(ctx.obj['output_path'], consortium_name, workspace_name)
        if workspace:
            data_store_name = ensure_data_store_name(workspace)
            print(workspace.workspace.name, data_store_name)
        else:
            logger.warning(("no.workspace", consortium_name, workspace_name))


@utility.command(name='ontologies')
@click.option('--consortium', default=None, help='Filter, only this consortium.')
@click.option('--workspace', default=None, help='Filter, only this workspace.')
@click.option('--details', default=False, help='Include error details.', show_default=True, is_flag=True)
@click.pass_context
def _ontologies(ctx, consortium, workspace, details):
    """Find ontologies fields workspace and write summary to stdout."""
    G = _recursive_default_dict()
    for ontology_fields in ontologies(ctx.obj['output_path'], consortium, workspace, details):
        for ontology_field in ontology_fields:
            G[ontology_field['consortium_name']][ontology_field['workspace_name']][ontology_field['entity_name']] = ontology_fields['ontology_fields']
    print(json.dumps(G))


@utility.command(name='qa')
@click.option('--consortium', default=None, help='Filter, only this consortium.')
@click.option('--workspace', default=None, help='Filter, only this workspace.')
@click.option('--details', default=False, help='Include error details.', show_default=True, is_flag=True)
@click.pass_context
def qa(ctx, consortium, workspace, details):
    """Report on analysis."""
    summaries = []
    with open(f"{ctx.obj['output_path']}/analysis.ndjson") as input_stream:
        for line in input_stream.readlines():
            summaries.append(json.loads(line))

