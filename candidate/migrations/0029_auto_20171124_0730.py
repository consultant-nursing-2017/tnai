# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-24 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0028_auto_20171124_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalqualifications',
            name='marks_obtained',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='additionalqualifications',
            name='percentage',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='additionalqualifications',
            name='total_marks',
            field=models.PositiveSmallIntegerField(blank=True, default=100, null=True),
        ),
        migrations.AlterField(
            model_name='educationalqualifications',
            name='marks_obtained',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='educationalqualifications',
            name='percentage',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='educationalqualifications',
            name='total_marks',
            field=models.PositiveSmallIntegerField(blank=True, default=100, null=True),
        ),
        migrations.AlterField(
            model_name='professionalqualifications',
            name='marks_obtained',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='professionalqualifications',
            name='percentage',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='professionalqualifications',
            name='total_marks',
            field=models.PositiveSmallIntegerField(blank=True, default=100, null=True),
        ),
    ]