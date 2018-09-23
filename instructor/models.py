from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from candidate.models import EligibilityTests
from tnai.validators import ValidateFileExtension
from hashid_field import HashidAutoField, HashidField
from django.conf import settings
from student.models import Student

import datetime
import uuid
import pdb

class Instructor(models.Model):
    instructor_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Instructor", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_username', default=None, blank=True, null=True)
    name = models.CharField(max_length=200, default="Instructor One", blank=False)

class Topic(models.Model):
    topic_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Topic", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    name = models.CharField(max_length=200, default="Topic One", blank=False, unique = True)

    def __str__(self):
        return self.name

class Question(models.Model):
    DIFFICULTY_CHOICES = (
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
    )
    question_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Question", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    def media_path(instance, filename):
        return 'instructor/questions/{0}/{1}'.format(str(instance.question_id), filename)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_for_question', default=None, blank=True, null=True)
    difficulty = models.CharField(max_length = 100, blank = True, choices = DIFFICULTY_CHOICES)
    text = models.CharField(max_length = 10000, blank=True)
    image = models.FileField(default=None, blank=True, null=True, upload_to=media_path, validators=[ValidateFileExtension.validate_image])

    def __str__(self):
        return self.truncated_text()

    def truncated_text(self):
        return self.text[:80]

    def answers(self):
        return Answer.objects.filter(question = self).order_by('text')

class Answer(models.Model):
    def media_path(instance, filename):
        return 'instructor/answers/{0}/{1}'.format(str(instance.answer_id), filename)

    answer_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Answer", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_for_answer', default=None, blank=True, null=True)
    text = models.CharField(max_length = 2000, blank=True)
    image = models.FileField(default=None, blank=True, null=True, upload_to=media_path, validators=[ValidateFileExtension.validate_image])
    correct = models.BooleanField(default = False)

    def __str__(self):
        return self.text

class QuestionBank(models.Model):
    question_bank_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"QuestionBank", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    name = models.CharField(max_length=200, default="Question Bank One", blank=False, unique = True)
    questions = models.ManyToManyField(Question)

class Exam(models.Model):
    exam_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Exam", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", primary_key = True)
    name = models.CharField(max_length=200, default="Exam One", blank=False, unique = True)
    date = models.DateField(blank = False)
    starting_time = models.TimeField(blank = False)
    duration = models.IntegerField(default = 30, blank = False)
    is_public = models.BooleanField(default = False, blank = False)
    students = models.ManyToManyField(Student, blank = True)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        public_string = ""
        if self.is_public:
            public_string = " (Public)"
        return self.name + public_string
