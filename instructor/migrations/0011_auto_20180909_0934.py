# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-09 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0010_auto_20180909_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='students',
            field=models.ManyToManyField(blank=True, to='student.Student'),
        ),
    ]
