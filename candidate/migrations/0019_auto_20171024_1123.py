# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-24 11:23
from __future__ import unicode_literals

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0018_auto_20171024_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='registration_number',
            field=hashid_field.field.HashidField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, min_length=7, null=True),
        ),
    ]
