# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-22 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0026_auto_20171120_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateNursingCouncilName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='statenursingcouncil',
            name='state',
        ),
        migrations.AddField(
            model_name='statenursingcouncil',
            name='state_nursing_council_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.StateNursingCouncilName'),
        ),
    ]
