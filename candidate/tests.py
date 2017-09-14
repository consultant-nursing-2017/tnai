from django.test import TestCase
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from employer.models import Employer
from .models import Candidate, EducationalQualifications, ProfessionalQualifications, AdditionalQualifications, EligibilityTests, Experience, StateNursingCouncil
from .forms import SubmitForm, PersonalForm, StateNursingCouncilForm, EducationalQualificationsForm, ProfessionalQualificationsForm, AdditionalQualificationsForm, EligibilityTestsForm, ExperienceForm, PassportAndMiscForm, StateNursingCouncilForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import SignupForm, EducationalQualificationsForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import pdb
import os
import hashlib
import random

# Create your tests here.

class PersonalFormTests(TestCase):
    def test_date_of_birth_must_be_in_the_past(self):
        time = timezone.now() + datetime.delta(days=30)
#        form = PersonalForm(initial=[{'date_of_birth': time}])
#        self.assertTrue(form.is_valid())
