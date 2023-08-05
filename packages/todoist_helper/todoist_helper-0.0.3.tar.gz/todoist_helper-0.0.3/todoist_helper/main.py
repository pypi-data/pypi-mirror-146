"""Main module."""
import click

from .add_todoist_task import add_todoist_task
from .add_obsidian_task import add_obsidian_task


@click.group()
def cli():
    """
    Main group.
    """


@click.command()
@click.option("-p", "--project_id")
def add(project_id):
    """
    Add a new todoist task to the inbox.
    """
    add_todoist_task(project_id)
    click.echo("Todoist task added.")


@click.command()
@click.option("-i", "--inbox_path", required=True)
def add_obsidian(inbox_path):
    """
    Add a new task to the Obsidian inbox document.
    """
    add_obsidian_task(inbox_path)


cli.add_command(add)
cli.add_command(add_obsidian)
