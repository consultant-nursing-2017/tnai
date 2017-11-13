from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from candidate.models import Candidate
from hashid_field import HashidAutoField

import datetime
import uuid


class Exam(models.Model):
    serial_id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=False, default="Exam1")
    date = models.DateField(blank=False, default=timezone.now)
    room = models.CharField(max_length=500, blank=False, default="Room1")
    notes = models.CharField(max_length=500, blank=True)

class ExamTimeSlots(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam', default=None, blank=True, null=True)
    begin_time = models.TimeField()
    end_time = models.TimeField()
    maximum_number_of_students = models.IntegerField(default=50)
    number_of_students_booked = models.IntegerField(default=0, editable=False)

class CandidateBookTimeSlot(models.Model)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(ExamTimeSlots, on_delete=models.CASCADE, related_name='time_slot', default=None, blank=True, null=True)

#class Profile(models.Model):
#    user = models.OneToOneField(User, related_name='employer_profile') #1 to 1 link with Django User
#    activation_key = models.CharField(max_length=40)
#    key_expires = models.DateTimeField()
