import click

from stoobly_agent.app.settings import Settings

from .report_facade import ReportFacade
from .utils.tabulate_print_service import tabulate_print

@click.group(
    epilog="Run 'stoobly-agent report COMMAND --help' for more information on a command.",
    help="Manage test reports"
)
@click.pass_context
def report(ctx):
    pass

@report.command(
    help="Create a report"
)
@click.option('--description', help='Report description.')
@click.option('--project-key', required=True, help='Project to create report in.')
@click.argument('name')
def create(**kwargs):
    report = ReportFacade(Settings.instance())
    print(report.create(kwargs['project_key'], kwargs['name'], kwargs['description']))

@report.command(
    help="Show created reports"
)
@click.option('--page', default=0)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.argument('project_key')
def list(**kwargs):
    report_key = kwargs['project_key']
    del kwargs['project_key']

    report = ReportFacade(Settings.instance())
    reports_response = report.index(report_key, **kwargs)
    
    tabulate_print(reports_response['list'], filter=['created_at', 'user_id', 'starred', 'updated_at'])