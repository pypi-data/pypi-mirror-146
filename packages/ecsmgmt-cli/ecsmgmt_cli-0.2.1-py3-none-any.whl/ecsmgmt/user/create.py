import click
from ecsclient.common.exceptions import ECSClientException

from .._util.exceptions import EcsmgmtClickException
from .._util.format import success_echo


@click.command()
@click.argument('user-id', type=click.STRING)
@click.option('-n', '--namespace', type=click.STRING, show_default=True)
@click.option(
    '-t', '--tag', 'tags',
    multiple=True,
    type=click.STRING,
    help='User tags seperated by ",", option can be provided multiple times'
)
@click.pass_obj
def cli(obj, user_id, namespace, tags):
    """Create new object user
    """
    client = obj['client']

    sane_tags = []
    for tag in tags:
        splited = tag.split(',')
        sane_tags.extend(splited)

    try:
        client.object_user.create(user_id=user_id, namespace=namespace, tags=sane_tags)
        success_echo(f'created user "{user_id}" in namespace "{namespace}"')
    except ECSClientException as e:
        raise EcsmgmtClickException(e.message)
