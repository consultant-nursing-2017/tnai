# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-29 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ra', '0006_auto_20171222_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatelist',
            name='exam_list_type',
            field=models.CharField(blank=True, choices=[('Showed interest', 'Showed interest'), ('Booked time slot', 'Booked time slot'), ('Downloaded hall ticket', 'Downloaded hall ticket')], max_length=100),
        ),
    ]
