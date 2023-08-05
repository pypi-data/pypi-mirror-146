import click
import os


@click.group()
def scans():
    """All types of scans"""
    pass


@scans.command(short_help="Default scan")
@click.pass_context
def default(ctx: click.Context):
    try:
        print("Performing default scan")
    except Exception as e:
        click.echo(click.style(f"Failed to perform default scan", fg="red"))


@scans.command(short_help="Quick scan")
@click.pass_context
def quick(ctx: click.Context):
    try:
        print("Performing quick scan")
    except Exception as e:
        click.echo(click.style(f"Failed to perform quick scan", fg="red"))
