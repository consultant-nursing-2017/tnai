# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-29 10:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0006_auto_20170829_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(blank=True, verbose_name=datetime.datetime(2017, 8, 29, 10, 4, 11, 287686, tzinfo=utc)),
        ),
    ]