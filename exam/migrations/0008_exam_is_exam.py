# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_candidatebooktimeslot_hall_ticket_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_exam',
            field=models.BooleanField(default=True),
        ),
    ]
