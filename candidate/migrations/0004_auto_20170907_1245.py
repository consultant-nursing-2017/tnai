# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-07 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_auto_20170907_0833'),
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
            model_name='eligibilitytests',
            name='score_grade_marks',
        ),
        migrations.RemoveField(
            model_name='professionalqualifications',
            name='grade',
        ),
    ]