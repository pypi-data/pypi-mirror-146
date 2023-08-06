import click
from ecsclient.common.exceptions import ECSClientException

from .._util.exceptions import EcsmgmtClickException
from .._util.format import success_echo, pretty_table


@click.command()
@click.argument('user-id')
@click.option('-n', '--namespace', type=click.STRING, show_default=True, help='Namespace of the user')
@click.option('-e', '--expiry-time', type=click.INT, help='Expiry time in minutes for the previous secret key.')
@click.option('-k', '--secret-key', type=click.STRING, help='Provide secret key instead of generating one.')
@click.pass_obj
def cli(obj, user_id, namespace, expiry_time, secret_key):
    """Create new secret key
    """
    client = obj['client']

    try:
        res = client.secret_key.create(user_id=user_id, namespace=namespace, expiry_time=expiry_time,
                                       secret_key=secret_key)
        data = [
            ('Secret Key:', res['secret_key']),
        ]
        msg = pretty_table(data, tablefmt='plain')
        if expiry_time is not None:
            res = client.secret_key.get(user_id=user_id, namespace=namespace)
            msg += f'\nOld secret key "{res["secret_key_1"]}" expires at "{res["key_expiry_timestamp_1"]}".'
        success_echo(f'Created secret key for user "{user_id}" in namespace "{namespace}":\n{msg}')
    except ECSClientException as e:
        raise EcsmgmtClickException(e.message)
