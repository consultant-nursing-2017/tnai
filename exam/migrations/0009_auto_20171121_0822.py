# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_exam_is_exam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='is_exam',
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_or_interview',
            field=models.CharField(choices=[('Exam', 'Exam'), ('Interview', 'Interview')], default='Exam', max_length=100),
        ),
    ]