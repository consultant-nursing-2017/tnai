# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-14 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0007_auto_20180414_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='questions',
            field=models.ManyToManyField(to='instructor.Question'),
        ),
    ]
