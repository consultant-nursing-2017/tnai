# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-14 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_takeexam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takeexam',
            name='exam',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exam_taken', to='instructor.Exam'),
        ),
    ]
