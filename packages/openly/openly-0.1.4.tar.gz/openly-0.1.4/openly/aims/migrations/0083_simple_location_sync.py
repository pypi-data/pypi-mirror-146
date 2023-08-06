from django.core.management import call_command
from django.db import migrations


def call_sync_translation_fields(*arga, **kwargs):
    call_command("sync_translation_fields", "--noinput")


class Migration(migrations.Migration):

    dependencies = [("aims", "0082_auto_20191204_0123")]

    operations = [
        # This turned out to be a Very Bad Idea.
        # It breaks following migrations.
        # Instead run as a post-migration hook in aims
        # migrations.RunPython(call_sync_translation_fields),
        # migrations.RunSQL(
        #     'UPDATE simple_locations_area SET name_en = name;'
        # ),
        # migrations.RunSQL(
        #     'UPDATE simple_locations_areatype SET name_en = name;'
        # )
    ]
