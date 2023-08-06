from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = 'Handles migrating data from from old->new Profiles tables'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.db_name = settings.DATABASES['default']['NAME']

    def handle(self, *args, **options):
        db_profile_tables = [
            {
                "v1": {"tbl": "profiles_organisationprofile", "cols": "id, url, logo, banner_image, banner_text, organisation_id"},
                "v2": {"tbl": "profiles_v2_organisationprofile", "cols": "id, url, logo, banner_image, banner_text, organisation_id"},
            },
            {
                "v1": {"tbl": "profiles_contact", "cols": "id, title, address, phone_number, email, organisation_profile_id, fax"},
                "v2": {"tbl": "profiles_v2_organisationcontactinfo", "cols": "id, title, address, phone_number, email, profile_id, fax"},
            },
            {
                "v1": {"tbl": "profiles_person", "cols": "*"},
                "v2": {"tbl": "profiles_v2_person", "cols": "*"},
            },
            {
                "v1": {"tbl": "profiles_organisationprofile", "cols": "id, background, \'en\', id"},
                "v2": {"tbl": "profiles_v2_organisationprofile_translation", "cols": "id, background, language_code, master_id"},
            },
        ]

        while True:
            answer = input(
                "Are you sure you want to do this? This will truncate and migrate profile tables! (Y/n): ").strip().lower()
            if answer == 'y':
                with connection.cursor() as cursor:
                    for tables in db_profile_tables:
                        self.truncate_table(cursor, tables)
                        self.fill_table(cursor, tables)
                    cursor.execute('''SELECT setval(pg_get_serial_sequence('"profiles_v2_organisationprofile_translation"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "profiles_v2_organisationprofile_translation";''')
                    cursor.execute('''SELECT setval(pg_get_serial_sequence('"profiles_v2_organisationprofile"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "profiles_v2_organisationprofile";''')
                    cursor.execute('''SELECT setval(pg_get_serial_sequence('"profiles_v2_organisationcontactinfo"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "profiles_v2_organisationcontactinfo";''')
                    cursor.execute('''SELECT setval(pg_get_serial_sequence('"profiles_v2_person"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "profiles_v2_person";''')
                return self.stdout.write(self.style.SUCCESS(
                    'Successfully migrated old --> new profiles data'))
            elif answer == 'n':
                return self.stdout.write(self.style.SUCCESS(
                    'Migration was aborted by user.'))
            else:
                self.stdout.write(self.style.ERROR(
                    "Input Error - Please enter 'y' or 'n'."))

    def truncate_table(self, cursor, tables):
        cursor.execute("""TRUNCATE TABLE %s CASCADE""" % tables['v2']['tbl'])

    def fill_table(self, cursor, tables):
        if tables['v1']['cols'] == "*" and tables['v2']['cols'] == "*":
            cursor.execute("""INSERT INTO %s SELECT * FROM %s""" %
                           (tables['v2']['tbl'], tables['v1']['tbl']))
        else:
            cursor.execute("""INSERT INTO %s (%s) SELECT %s FROM %s""" %
                           (tables['v2']['tbl'], tables['v2']['cols'], tables['v1']['cols'], tables['v1']['tbl']))
