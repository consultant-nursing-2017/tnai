from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from candidate.models import Candidate
from hashid_field import HashidAutoField, HashidField
from django.conf import settings
from employer.models import Advertisement

import datetime
import uuid

# Exam should be understood as representing "Exam/Interview"

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
            ("Written + Interview", "Written + Interview"),
            ("Only Interview", "Only Interview"),
    ]

    exam_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Exam", primary_key=True, allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='advertisement', blank=False, null=True)
    exam_type = models.CharField(max_length=100, choices=EXAM_TYPE_CHOICES, blank=True, default="Only Interview")
    name = models.CharField(max_length=500, blank=False, default="Exam1")
    date = models.DateField(blank=False, default=timezone.now)
    hall_ticket_download_last_date = models.DateField(blank=False, default=timezone.now)

    def __str__(self):
        return "Exam: " + self.name + " Exam ID: " + str(self.exam_id)

    @staticmethod
    def exam_type_choices():
        return Exam.EXAM_TYPE_CHOICES

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
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_book_slot', default=None, blank=True, null=True)
    time_slot = models.ForeignKey(ExamTimeSlot, on_delete=models.CASCADE, related_name='time_slot', default=None, blank=True, null=True)
    exam_room = models.ForeignKey(ExamRoom, on_delete=models.CASCADE, related_name='exam_room', default=None, blank=True, null=True)
    hall_ticket_number = HashidField(salt=settings.HASHID_FIELD_SALT+"Hall ticket", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEF", null=True)
    hall_ticket_downloaded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(CandidateBookTimeSlot, self).save(*args, **kwargs)
        if not self.hall_ticket_number:
            self.hall_ticket_number = self.pk
        super(CandidateBookTimeSlot, self).save(*args, **kwargs)

#class Profile(models.Model):
#    user = models.OneToOneField(User, related_name='employer_profile') #1 to 1 link with Django User
#    activation_key = models.CharField(max_length=40)
#    key_expires = models.DateTimeField()
