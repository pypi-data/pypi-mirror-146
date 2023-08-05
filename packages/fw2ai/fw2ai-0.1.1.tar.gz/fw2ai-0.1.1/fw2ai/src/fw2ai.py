import click
from main.commands import scans 

@click.group()
@click.version_option(package_name="fw2ai")
@click.option(
    "--debug", type=click.BOOL, default=False, is_flag=True, help="Enable debug logging"
)
@click.pass_context
def cli(ctx: click.Context, debug: bool):
    print("Entry point for fw2ai")



cli.add_command(scans)