# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-23 09:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0009_auto_20171018_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='closing_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 22, 9, 59, 17, 292513, tzinfo=utc)),
        ),
    ]
