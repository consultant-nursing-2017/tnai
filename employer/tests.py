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
from .models import Employer
from .forms import SignupForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.management import call_command

import pdb
import os
import hashlib
import random
import datetime

# Create your tests here.

class EmployerSignupViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'prod_data', verbosity=0)


    def test_signup_form_should_have_both_passwords_match(self):
        """ 
        Signup form should have both passwords match
        """
        form = SignupForm({'username': 'Anand.84@gmail.com', 'password1': 'abc xyz1', 'password2': 'abc xyz2'})
        self.assertFalse(form.is_valid())

        form = SignupForm({'username': 'abc1234567', 'password1': 'abcd xyz1', 'password2': 'abcd xyz1'})
        self.assertTrue(form.is_valid())

    def test_login_username_should_be_case_insensitive(self):
        """ 
        Candidate login username should be case insensitive
        """
        form = SignupForm({'username': 'Consultant.nursing.2017@gmail.com', 'password1': 'candidate1', 'password2': 'candidate1'})
        self.assertFalse(form.is_valid())
