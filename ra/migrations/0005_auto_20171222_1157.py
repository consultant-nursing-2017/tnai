# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-22 11:57
from __future__ import unicode_literals

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('ra', '0004_candidatelist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatelist',
            name='id',
        ),
        migrations.AddField(
            model_name='candidatelist',
            name='list_id',
            field=hashid_field.field.HashidAutoField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', default=None, editable=False, min_length=7, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]