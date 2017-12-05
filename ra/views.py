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
from candidate.models import Candidate, StateNursingCouncilName
from employer.models import Employer
from employer.models import Advertisement
from .forms import FilterForm
from candidate.forms import StateNursingCouncilNameForm
from .models import RA
from .forms import ActAsForm

import pdb

def is_allowed(username, request):
    allowed = True
    if username.groups.filter(name="TNAI").count() <= 0:
        allowed = False
    
    return allowed

def ra_index(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)
    else:
        ra_not_found = False
        try:
            ra = RA.objects.get(logged_in_as=username)
        except ObjectDoesNotExist:
            ra = RA.objects.create(logged_in_as=username, acting_as=None)
        return render(request, 'ra/index.html', {'ra': ra, }) 

def candidate_list(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    queryset = Candidate.objects.all()
    if request.method == 'POST':
        if 'clear_all_filters' in request.POST:
            filter_form = FilterForm()
        else:
            filter_form = FilterForm(request.POST)
            if filter_form.is_valid():
                name = filter_form.cleaned_data['name']
                if name is not None and len(name) > 0:
                    queryset = queryset.filter(name__icontains=name)
                date_of_birth = filter_form.cleaned_data['date_of_birth']
                if date_of_birth is not None:
                    queryset = queryset.filter(date_of_birth=date_of_birth)
                gender = filter_form.cleaned_data['gender']
                if gender is not None:
                    queryset = queryset.filter(gender=gender)
    else:
        filter_form = FilterForm()

    return render(request, 'ra/candidate_list.html', {'queryset': queryset, 'filter_form': filter_form, }, )

def employer_list(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    queryset = Employer.objects.all()
    return render(request, 'ra/employer_list.html', {'queryset': queryset}, )

def advertisement_list(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    queryset = Advertisement.objects.all()
    return render(request, 'ra/advertisement_list.html', {'queryset': queryset}, )

def edit_list_state_nursing_council(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    queryset = StateNursingCouncilName.objects.all().order_by('name')
    if request.method == 'POST':
        form = StateNursingCouncilNameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ra/edit_list_state_nursing_council/')
    else:
        form = StateNursingCouncilNameForm()

    return render(request, 'ra/edit_list_state_nursing_council.html', {'queryset': queryset, 'form': form, })

def verify_candidate(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    if request.method == 'GET':
        registration_number = request.GET.__getitem__('registration_number')
        try:
            candidate = Candidate.objects.get(registration_number=registration_number)
        except ObjectDoesNotExist:
            return render(request, 'ra/invalid_registration_number.html', {'registration_number': registration_number}, )

        return render(request, 'ra/verify_candidate.html', {'candidate': candidate}, )
    else:
        if 'verify_yes' in request.POST:
            registration_number = request.POST.get('registration_number')
            candidate = Candidate.objects.get(registration_number=registration_number)
            candidate.is_provisional_registration_number = False
            candidate.save()
            return HttpResponseRedirect('/candidate/candidate_profile?registration_number='+str(registration_number))
        else:
            return HttpResponseRedirect('/ra/')

def act_as(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)
    ra = RA.objects.get(logged_in_as=username)

    if request.method == 'POST':
        form = ActAsForm(request.POST, instance=ra)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect('/ra/')
    else:
        form = ActAsForm(instance=ra)

    return render(request, 'ra/act_as.html', {'form': form}, )
