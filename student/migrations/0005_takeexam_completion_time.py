# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-25 04:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20180414_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='takeexam',
            name='completion_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]