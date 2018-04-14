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
from .models import Student
from .forms import StudentForm
#from .forms import RegistrationForm
from django.core.mail import send_mail
import hashlib
import random
import pdb
from django.utils.crypto import get_random_string
from django.contrib import auth

from django.shortcuts import render, redirect
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

def is_student_user(username, request):
    student_user = True
    if username.groups.filter(name="Student").count() <= 0:
        student_user = False
    
    return student_user

def is_allowed(username, request):
    allowed = is_student_user(username, request)
    return allowed

def get_acting_user(request):
    username=auth.get_user(request)
    return username

def index(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    object_does_not_exist = False
    if username.groups.filter(name="Candidate").count() > 0:
        return HttpResponseRedirect('/candidate/')

    try:
        if username.is_authenticated():
            student = Student.objects.get(username=username)
        else:
            student = None
    except ObjectDoesNotExist:
        student = None
        object_does_not_exist = True

    return render(request, 'student/index.html', {'student': student, 'object_does_not_exist': object_does_not_exist, }) 

def submit_student(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    new_profile = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            student = Student.objects.get(username=username)
            new_profile = False
            form = StudentForm(request.POST, request.FILES, instance=student)
        except ObjectDoesNotExist:
            new_profile = True
            form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/student/')
    else:
        # if a GET (or any other method) we'll create a blank form
        try:
            student = Student.objects.get(username=username)
            form = StudentForm(instance=student)
            new_profile = False
        except ObjectDoesNotExist:
            new_profile = True
            form = StudentForm(initial={'username': username,})

    return render(request, 'student/submit_student.html', {'new_profile': new_profile, 'form': form,}) 
