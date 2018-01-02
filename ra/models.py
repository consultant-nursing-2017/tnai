from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tnai.validators import ValidateFileExtension
from hashid_field import HashidAutoField, HashidField
from django.conf import settings

from candidate.models import Candidate
from employer.models import Employer, Advertisement
from exam.models import Exam

import datetime
import uuid

class RA(models.Model):
    logged_in_as = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_in_as', default=None, blank=True, null=True)
    acting_as = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acting_as', default=None, blank=True, null=True)
    def __str__(self):
        if self.acting_as is not None:
            return self.logged_in_as.username + " (acting as: " + self.acting_as.username + ")"
        else:
            return self.logged_in_as.username + " (as SuperUser)"

class CandidateList(models.Model):
    EXAM_LIST_TYPE_CHOICES = (
        ("Showed interest", "Showed interest"),
        ("Booked time slot", "Booked time slot"),
        ("Downloaded hall ticket", "Downloaded hall ticket"),
    )
    list_id = HashidAutoField(salt=settings.HASHID_FIELD_SALT+"Candidate List", primary_key=True, allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    name = models.CharField(max_length = 200, blank=False)
    members = models.ManyToManyField(Candidate) #, through='CandidateListMembership')
    time_created = models.DateTimeField(default=timezone.datetime.now, editable = False)
    notes = models.CharField(max_length = 500, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, default=None, blank=True, null=True)
    exam_list_type = models.CharField(max_length = 100, choices = EXAM_LIST_TYPE_CHOICES, blank = True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return ', '.join((self.name, self.exam_list_type, str(self.time_created), str(self.exam), str(self.employer), str(self.advertisement)))

#class CandidateListMembership(models.Model):
#    candidate_list = models.ForeignKey(CandidateList, on_delete=models.CASCADE)
#    candidate_list_member = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_list_member')
