# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.core.management import call_command
from django.db import migrations


# this disabled due to adding a update_translation_fields call later in the migration list
# def load_fixture(apps, schema_editor):
#    call_command('loaddata', 'iati_objects_required', app_label='aims')


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0004_auto_20160811_0345'),
        ('iati', '0011_auto_20170418_1526'),
    ]

    operations = [
        # this disabled due to adding a update_translation_fields call later in the migration list
        # migrations.RunPython(load_fixture)
    ]
