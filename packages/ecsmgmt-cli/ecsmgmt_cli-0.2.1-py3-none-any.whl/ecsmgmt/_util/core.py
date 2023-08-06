"""Implements enhancments for click core utilities"""

import importlib
import os

import click


class DynamicMultiCommandFactory:
    """A factory to make configurable dynamic click.MultiCommand

    The main purpose of the factory is the configuration of the dynamic click.MultiCommand.
    It is a quirk, but currently there is no better implentation for this purpose.
    Feel free to find a better solution.
    """

    def create(self, parent_path, base_package):
        """Create a DynamicMultiCommand and uses parent_path as search path.

        Keyword arguments:
        parent_path -- search parent_path for sub commands
        base_package -- base package from where the subcommands are imported
        """

        # strip parent filename from path
        plugin_path = os.path.dirname(parent_path)

        class DynamicMultiCommand(click.MultiCommand):
            """A dynamic Multicommand implementation of click.MultiCommand

            Commands are dynamically """

            def list_commands(self, ctx):
                commands = []
                for pathname in os.listdir(plugin_path):
                    if pathname.startswith('_'):
                        continue

                    if pathname.endswith('.py'):
                        commands.append(pathname[:-3])
                    elif os.path.isdir(os.path.join(plugin_path, pathname)):
                        commands.append(pathname)

                commands.sort()
                return commands

            def get_command(self, ctx, cmd_name):
                commands = self.list_commands(ctx)
                command_candidates = [c for c in commands if c.startswith(cmd_name)]

                if len(command_candidates) == 1:
                    command = command_candidates[0]
                elif len(command_candidates) > 1:
                    ctx.fail("Too many command matches: {matches}".format(
                        matches=', '.join(sorted(command_candidates))))
                else:
                    command = None

                if command is None:
                    return_command = None
                else:
                    try:
                        command_module = importlib.import_module(".{name}".format(name=command), base_package)
                        return_command = command_module.cli
                    except ModuleNotFoundError:
                        return_command = None

                return return_command

        return DynamicMultiCommand
