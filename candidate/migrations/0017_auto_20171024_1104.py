# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-24 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0016_auto_20171023_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='is_provisional_registration_number',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='candidate',
            name='registration_number',
            field=hashid_field.field.HashidField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, null=True),
        ),
    ]