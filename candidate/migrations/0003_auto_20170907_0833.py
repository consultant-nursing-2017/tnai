# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-07 08:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_auto_20170907_0629'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='tnai_number',
            new_name='TNAI_number',
        ),
    ]