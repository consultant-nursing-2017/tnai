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
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

import pdb
import os
import hashlib
import random

##from django.contrib.auth.decorators import permission_required


def index(request):
    current_site = get_current_site(request)
    if current_site == 'http://132.148.247.155':
        return HttpResponseRedirect('/student/learning-index/')
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def recruitment(request):
    return render(request, 'home/recruitment.html')

def contact(request):
    return render(request, 'home/contact.html')

def media(request):
    return render(request, 'home/media.html')

def success_msg(request):
    success_msg = "Success message not found!"
    if request.method == 'GET':
        try:
            success_msg = request.GET.get('success_msg')
        except KeyError:
            success_msg = "Error message not found!"

    return render(request, 'home/success_msg.html', {'success_msg': success_msg})

def error_msg(request):
    error_msg = "Error message not found!"
    if request.method == 'GET':
        try:
            error_msg = request.GET.get('error_msg')
        except KeyError:
            error_msg = "Error message not found!"

    return render(request, 'home/error_msg.html', {'error_msg': error_msg})
