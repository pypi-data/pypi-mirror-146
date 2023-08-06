import click
from ecsclient.common.exceptions import ECSClientException

import inquirer

from .._util.format import success_echo
from .._util.exceptions import EcsmgmtClickException


@click.command()
@click.argument('user-id')
@click.option('-n', '--namespace', type=click.STRING, show_default=True, help='Namespace of the user')
@click.option('-k', '--secret-key', type=click.STRING, help='Secret key which should get deleted')
@click.pass_obj
def cli(obj, user_id, namespace, secret_key):
    """Deletes secret key
    """
    client = obj['client']

    res = client.secret_key.get(user_id=user_id, namespace=namespace)
    existing_secret_keys = []
    for i in [1, 2]:
        if res[f'secret_key_{i}_exist']:
            existing_secret_keys.append(res[f'secret_key_{i}'])

    # abort if no keys are present
    if not existing_secret_keys:
        raise EcsmgmtClickException(f'User "{user_id}" in namespace "{namespace}" has no secret keys set.')

    if len(existing_secret_keys) > 1 and secret_key is None:
        secret_key_options = [
            inquirer.Checkbox(
                'secret_keys_to_delete',
                message=f'User "{user_id}" in namespace "{namespace}" has both secret keys set, which should be deleted?',
                choices=existing_secret_keys,
            )
        ]
        answers = inquirer.prompt(secret_key_options)
        secret_keys_to_delete = answers['secret_keys_to_delete']

        if len(secret_keys_to_delete) == 0:
            click.echo("Nothing was deleted!")
            return
    # abort if given secret_key is not assigned to user
    elif secret_key is not None and secret_key not in existing_secret_keys:
        raise EcsmgmtClickException(f'User "{user_id}" in namespace "{namespace}" has no secret key "{secret_key}".')
    else:
        secret_keys_to_delete = existing_secret_keys

    try:
        if len(secret_keys_to_delete) == 2:
            client.secret_key.delete(user_id=user_id, namespace=namespace, secret_key=None)
        else:
            for key in secret_keys_to_delete:
                client.secret_key.delete(user_id=user_id, namespace=namespace, secret_key=key)
        key_list = ", ".join([f'"{item}"' for item in secret_keys_to_delete])
        success_echo(f'Deleted secret-keys {key_list} from user "{user_id}" in namespace "{namespace}"')
    except ECSClientException as e:
        raise EcsmgmtClickException(e.message)
