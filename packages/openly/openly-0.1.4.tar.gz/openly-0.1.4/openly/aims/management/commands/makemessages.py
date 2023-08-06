import os
from importlib import import_module

from django.conf import settings
from django.core.management.commands.makemessages import Command as BaseMakemessages


class Command(BaseMakemessages):
    help = '''This command inherits from the base django makemessages to default to not add location lines ( use --do-location to turn this back on ) and allow makemessages for a single app ( or app list ) by changing directory to that app dir before running base functionality
    '''

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--do-location', action='store_true', dest='do_location',
                            default=False, help="Do write '#: filename:line' lines.")
        # allow the apps parameter to be an empty list, as well as one or more app label.
        parser.add_argument('apps', nargs='*', choices=tuple(settings.INSTALLED_APPS) + (tuple(),))

    def handle(self, *args, **options):
        self.stdout.write("running the openly makemessages command - see help for details\n")
        options['no_location'] = not options.get('do_location')

        if len(options['apps']):
            for app in options['apps']:
                module = import_module(app)
                self.stdout.write("processing app %s\n" % app)
                os.chdir(os.path.dirname(module.__file__))
                super(Command, self).handle(*args, **options)
        else:
            super(Command, self).handle(*args, **options)
