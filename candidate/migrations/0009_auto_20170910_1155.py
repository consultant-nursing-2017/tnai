# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-10 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0008_auto_20170910_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalqualifications',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='educationalqualifications',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='professionalqualifications',
            name='grade',
        ),
    ]