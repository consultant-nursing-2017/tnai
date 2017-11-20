# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-20 12:10
from __future__ import unicode_literals

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_auto_20171118_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatebooktimeslot',
            name='hall_ticket_number',
            field=hashid_field.field.HashidField(alphabet='0123456789ABCDEF', editable=False, min_length=7, null=True),
        ),
    ]
