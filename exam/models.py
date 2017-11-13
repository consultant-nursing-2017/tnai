from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from candidate.models import Candidate
from hashid_field import HashidAutoField

import datetime
import uuid


class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
            ("MOH", "MOH"),
            ("Prometric/HAAD", "Prometric/HAAD"),
    )
    exam_id = HashidAutoField(primary_key=True)
    exam_type = models.CharField(max_length=100, choices=EXAM_TYPE_CHOICES, blank=False, default="MOH")
    name = models.CharField(max_length=500, blank=False, default="Exam1")
    date = models.DateField(blank=False, default=timezone.now)
#    notes = models.CharField(max_length=500, blank=True)

class ExamTimeSlot(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam', default=None, blank=True, null=True)
    begin_time = models.TimeField()
    end_time = models.TimeField()
    maximum_number_of_students = models.IntegerField(default=200)
    number_of_students_booked = models.IntegerField(default=0, editable=False)

class ExamRoom(models.Model):
    exam_time_slot = models.ForeignKey(ExamTimeSlot, on_delete=models.CASCADE, related_name='exam_time_slot', default=None, blank=True, null=True)
    room_number = models.CharField(max_length=100, default="Room1")

class CandidateBookTimeSlot(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='candidate', on_delete=models.CASCADE)
    time_slot = models.ForeignKey(ExamTimeSlot, on_delete=models.CASCADE, related_name='time_slot', default=None, blank=True, null=True)
    exam_room = models.ForeignKey(ExamRoom, on_delete=models.CASCADE, related_name='exam_room', default=None, blank=True, null=True)

#class Profile(models.Model):
#    user = models.OneToOneField(User, related_name='employer_profile') #1 to 1 link with Django User
#    activation_key = models.CharField(max_length=40)
#    key_expires = models.DateTimeField()
