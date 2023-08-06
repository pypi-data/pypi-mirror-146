from django.core.management.commands.compilemessages import (
    Command as BaseCompilemessages,
)

help = """This command inherits from the base django compilemessages to default to not use --check-format so that translations in languages which don't require placeholders can still be compiled
"""
Command = type("Command", (BaseCompilemessages,), dict(program_options=[], help=help))
