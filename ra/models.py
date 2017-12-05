from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tnai.validators import ValidateFileExtension
from hashid_field import HashidAutoField, HashidField
from django.conf import settings

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
