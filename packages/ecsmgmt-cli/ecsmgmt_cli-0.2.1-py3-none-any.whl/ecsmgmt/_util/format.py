import click
from tabulate import tabulate


def pretty_table(data: list, headers: list = None, tablefmt: str = 'github') -> str:
    """Tabulate wrapper function with predefined format"""
    if headers is None:
        table = tabulate(data, tablefmt=tablefmt)
    else:
        table = tabulate(data, headers=headers, tablefmt=tablefmt)
    return table


def success_echo(message: str):
    click.secho('Success: ', nl=False, fg='green', bold=True)
    click.echo(message)
