# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0002_auto_20151021_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='openly_status',
            field=models.CharField(default=b'iatixml', max_length=12, choices=[(b'iatixml', 'IATI XML'), (b'draft', 'Draft'), (b'published', 'Published'), (b'archived', 'Archived')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='openly_status',
            field=models.CharField(default=b'iatixml', max_length=12, choices=[(b'iatixml', 'IATI XML'), (b'draft', 'Draft'), (b'published', 'Published'), (b'archived', 'Archived')]),
        ),
    ]
