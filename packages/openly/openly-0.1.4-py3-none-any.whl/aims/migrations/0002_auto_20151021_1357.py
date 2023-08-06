# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='completion',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='openly_status',
            field=models.CharField(default=b'iatixml', max_length=12, choices=[(b'iatixml', 'IATI XML'), (b'draft', 'Draft'), (b'published', 'Published')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='openly_status',
            field=models.CharField(default=b'iatixml', max_length=12, choices=[(b'iatixml', 'IATI XML'), (b'draft', 'Draft'), (b'published', 'Published')]),
        ),
    ]
