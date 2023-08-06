import click

from .._util.format import pretty_table


@click.command()
@click.pass_obj
def cli(obj):
    """List existing users
    """
    client = obj['client']

    user_request = client.object_user.list()
    user_list = [(entry['namespace'], entry['userid']) for entry in user_request['blobuser']]
    headers = ['Namespace', 'User ID']
    table = pretty_table(user_list, headers)
    click.echo(table)
