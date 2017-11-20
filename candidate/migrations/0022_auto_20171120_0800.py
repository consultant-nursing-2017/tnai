# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-20 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0021_auto_20171120_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='passport_valid_from',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='passport_valid_to',
        ),
        migrations.AddField(
            model_name='candidate',
            name='passport_valid_from',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='passport_valid_to',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
