import datetime

import click

from .._util.format import success_echo, pretty_table


@click.command()
@click.argument('user-id')
@click.option('-n', '--namespace', type=click.STRING, show_default=True)
@click.pass_obj
def cli(obj, user_id, namespace):
    """Get a users secret key
    """
    client = obj['client']

    res = client.secret_key.get(user_id=user_id, namespace=namespace)
    data = []
    for i in [1, 2]:
        if res[f'secret_key_{i}_exist']:
            if res[f'key_expiry_timestamp_{i}'] != '':
                timestamp = datetime.datetime.fromisoformat(res[f'key_expiry_timestamp_{i}'] + '+00:00')
                local_timestamp = timestamp.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
            else:
                local_timestamp = 'None'
            data.extend([
                (f'({i}) Secret Key', res[f'secret_key_{i}']),
                (f'({i}) Expiry Timestamp', local_timestamp)
            ])
    msg = pretty_table(data, tablefmt='plain')
    if data:
        success_echo(f'Secret keys for user "{user_id}" in namespace "{namespace}":\n{msg}')
    else:
        click.echo(f'User "{user_id}" in namespace "{namespace}" has no secret keys.')
