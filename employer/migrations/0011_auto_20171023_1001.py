# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-23 10:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0010_auto_20171023_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='closing_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 22, 10, 1, 6, 725571, tzinfo=utc)),
        ),
    ]
