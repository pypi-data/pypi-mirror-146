from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = 'Ensure clean cut over to new v2 Profiles, by dropping the old v1 tables from the DB'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.db_name = settings.DATABASES['default']['NAME']

    def handle(self, *args, **options):
        while True:
            answer = input(
                "Are you sure you want to do this? This will DROP all old v1 profile tables! (Y/n): ").strip().lower()
            if answer == 'y':
                with connection.cursor() as cursor:
                    old_tables = ['profiles_person', 'profiles_contact', 'profiles_organisationprofile']
                    for table in old_tables:
                        self.drop_table(cursor, table)
                return self.stdout.write(self.style.SUCCESS(
                    'Successfully dropped old v1 profiles tables from the DB.'))
            elif answer == 'n':
                return self.stdout.write(self.style.SUCCESS(
                    'Command was aborted by user.'))
            else:
                self.stdout.write(self.style.ERROR(
                    "Input Error - Please enter 'y' or 'n'."))

    def drop_table(self, cursor, table_name):
        cursor.execute("""DROP TABLE IF EXISTS %s""" % table_name)
