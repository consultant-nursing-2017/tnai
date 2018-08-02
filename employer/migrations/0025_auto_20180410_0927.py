# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-10 09:27
from __future__ import unicode_literals

from django.db import migrations, models
import tnai.validators


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0024_auto_20180103_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='authorized_signatory_id_proof',
            field=models.FileField(blank=True, default=None, max_length=500, null=True, upload_to='', validators=[tnai.validators.ValidateFileExtension.validate_file]),
        ),
        migrations.AlterField(
            model_name='employer',
            name='registration_certification',
            field=models.FileField(blank=True, default='', max_length=500, null=True, upload_to='', validators=[tnai.validators.ValidateFileExtension.validate_file]),
        ),
    ]