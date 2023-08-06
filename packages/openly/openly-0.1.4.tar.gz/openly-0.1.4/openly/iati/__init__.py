from django.conf import settings
from django.core.management import call_command
try:
    from haystack.management.commands.rebuild_index import Command
except:
    Command = None


''' Monkeypatch the rebuild_index management command for openly instances so that we correctly
    build the different search backends for each supported language.
'''


def handle_default(self, **options):
    if not Command:
        print("Haystack is not installed, exiting")
        return
    options.pop('workers')
    options.pop('batchsize')
    options.pop('interactive')
    if (
        hasattr(settings, "HAYSTACK_CONNECTIONS")
        and "default" in settings.HAYSTACK_CONNECTIONS
        and len(options["using"]) == 0
    ):
        options['using'].append('default')
        print('*************************************************\n'
              'ALERT: Running a monkeypatched version of rebuild_index! In openly projects '
              'multiple backends are used to support multilingual searches. The "default" '
              'connection is responsible for building the other indexes, so unless a different '
              'connection is specified (use the -u flag) only the "default" index is rebuilt. '
              'The monkeypatch code is located in iati/__init__.py\n'
              '*************************************************\n')
    # call_command('clear_index', **options)
    call_command('update_index', **options)

if Command:
    Command.handle = handle_default
