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
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
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

class RALoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'prod_data', verbosity=0)

    def test_login_username_should_be_case_insensitive(self):
        """ 
        RA login username should be case insensitive
        """
        self.client.post('/accounts/login/', {'username': 'Ra-user1', 'password': 'tnai ra user1'})
        response = self.client.get('/ra/')
        self.assertContains(response, "List all")

    def test_login_username_should_be_an_RA(self):
        """ 
        RA login username should be an RA
        """
        candidate_user = User.objects.get(username='consultant.nursing.2017@gmail.com')
        self.client.force_login(user=candidate_user)
        response = self.client.get('/ra/')
        self.assertContains(response, "not allowed")

        ra_user = User.objects.get(username='ra-user1')
        self.client.force_login(user=ra_user)
        response = self.client.get('/ra/')
        self.assertContains(response, "List all")

#    def test_signup_form_should_have_both_passwords_match(self):
#        """ 
#        Signup form should have both passwords match
#        """
#        form = SignupForm({'username': 'Anand.84@gmail.com', 'password1': 'abc xyz1', 'password2': 'abc xyz2'})
#        self.assertFalse(form.is_valid())
#
#        form = SignupForm({'username': 'abc1234567', 'password1': 'abcd xyz1', 'password2': 'abcd xyz1'})
#        self.assertTrue(form.is_valid())
#
#    def test_login_username_should_be_case_insensitive(self):
#        """ 
#        Candidate login username should be case insensitive
#        """
#        form = SignupForm({'username': 'Consultant.nursing.2017@gmail.com', 'password1': 'candidate1', 'password2': 'candidate1'})
#        self.assertFalse(form.is_valid())
