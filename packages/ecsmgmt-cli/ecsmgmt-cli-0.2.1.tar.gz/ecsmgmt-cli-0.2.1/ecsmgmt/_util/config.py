import os.path

import yaml


def load_config(ctx, param, config_path):
    configpath = os.path.abspath(os.path.expanduser(config_path))

    try:
        with open(configpath, 'r') as infile:
            config = yaml.safe_load(infile.read())
    except FileNotFoundError:
        return

    options = dict(config.pop('defaults', {}))

    try:
        namespace_functions = {
            'user': ['get', 'create', 'delete'],
            'secret-key': ['list', 'create', 'delete'],
        }
        namespace_options = {group: {command: {'namespace': options['namespace']} for command in commands} for
                             group, commands in namespace_functions.items()}
        options.update(namespace_options)
    except KeyError:
        pass

    ctx.default_map = options
    ctx.obj = {
        'config': config,
    }
