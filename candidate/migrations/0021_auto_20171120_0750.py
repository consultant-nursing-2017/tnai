# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-20 07:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0020_auto_20171116_0402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educationalqualifications',
            old_name='year_from',
            new_name='year_completed',
        ),
        migrations.RemoveField(
            model_name='educationalqualifications',
            name='year_to',
        ),
    ]
