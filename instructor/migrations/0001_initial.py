# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-05 11:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field
import instructor.models
import tnai.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', hashid_field.field.HashidAutoField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, min_length=7, primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=2000)),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=instructor.models.Answer.media_path, validators=[tnai.validators.ValidateFileExtension.validate_image])),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('instructor_id', hashid_field.field.HashidAutoField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, min_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Instructor One', max_length=200)),
                ('username', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instructor_username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', hashid_field.field.HashidAutoField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, min_length=7, primary_key=True, serialize=False)),
                ('difficulty', models.CharField(blank=True, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10000)),
                ('text', models.CharField(blank=True, max_length=10000)),
                ('image', models.FileField(blank=True, default=None, null=True, upload_to=instructor.models.Question.media_path, validators=[tnai.validators.ValidateFileExtension.validate_image])),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('instructor_id', hashid_field.field.HashidAutoField(alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, min_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Topic One', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_for_question', to='instructor.Topic'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_for_answer', to='instructor.Question'),
        ),
    ]
