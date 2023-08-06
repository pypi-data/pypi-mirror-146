from stactools.cli.registry import Registry


def register_plugin(registry: Registry) -> None:
    # Register subcommands

    from stactools.browse import commands

    registry.register_subcommand(commands.browse_command)


__version__ = "0.1.7"
