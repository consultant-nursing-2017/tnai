from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tnai.validators import ValidateFileExtension
from hashid_field import HashidAutoField, HashidField
from django.conf import settings

import datetime
import uuid
import pdb

class Student(models.Model):
    student_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Student", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_username', default=None, blank=True, null=True)
    name = models.CharField(max_length=200, default="Student One", blank=False)
    phone = models.CharField(max_length=200, default="9810117638", blank=False)

    def __str__(self):
        return self.name

class TakeExam(models.Model):
    exam = models.OneToOneField('instructor.Exam', on_delete=models.CASCADE, related_name='exam_taken')
    current_question = models.PositiveSmallIntegerField(default = 0)
    answers_given = models.ManyToManyField('instructor.Answer')
    completed = models.BooleanField(default = False)
