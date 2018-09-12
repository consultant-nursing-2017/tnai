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
    roll_number = models.CharField(max_length = 100, blank = True)
    email = models.CharField(max_length = 500, blank = True)

    def __str__(self):
        return self.name

class TakeExam(models.Model):
    take_exam_id = HashidField(salt=settings.HASHID_FIELD_SALT+"Exam", allow_int_lookup=True, null=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", default=None)
    exam = models.ForeignKey('instructor.Exam', on_delete=models.CASCADE, related_name='exam_taken')
    current_question = models.PositiveSmallIntegerField(default = 0)
    answers_given = models.ManyToManyField('instructor.Answer')
    completed = models.BooleanField(default = False)
    completion_time = models.DateTimeField(default = None, null = True)

    def save(self, *args, **kwargs):
        super(TakeExam, self).save(*args, **kwargs)
        if not self.take_exam_id:
            self.take_exam_id = self.pk
        super(TakeExam, self).save(*args, **kwargs)

    def score(self):
        take_exam = self
        exam = self.exam
        answers_given = self.answers_given.all()
        question_queryset = exam.questions.all()
        score = 0
        for question in question_queryset:
            count_answer = 0
            answer_queryset = question.answers()
            for answer in answer_queryset:
                answer_key = 0
                if answer.correct:
                    answer_key = answer_key + 1
                if answer in answers_given:
                    score = score + (4.0/3.0) * answer_key - (1.0/3.0)
                    answer_key = answer_key + 2
                count_answer = count_answer + 1

        return score
