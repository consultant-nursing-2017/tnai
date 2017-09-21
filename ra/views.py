from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
#from .forms import RegistrationForm
from django.core.mail import send_mail
import hashlib
import random
from django.utils.crypto import get_random_string
from django.contrib import auth

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def ra_index(request):
    username = auth.get_user(request)
    allowed = True
    if username.groups.filter(name="TNAI").count() <= 0:
        allowed = False
#        return HttpResponseRedirect('/accounts/logout/')

    return render(request, 'ra/index.html', {'username': username, 'allowed': allowed, }) 

def candidate_list(request):
    pass

def employer_list(request):
    pass