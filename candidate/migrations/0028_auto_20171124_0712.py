# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-24 07:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0027_auto_20171122_0753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eligibilitytests',
            old_name='eligibility_proof',
            new_name='proof',
        ),
    ]