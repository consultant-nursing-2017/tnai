from django.shortcuts import render

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
from candidate.models import Candidate
from .models import Exam, ExamTimeSlot, CandidateBookTimeSlot
from .forms import ExamForm, ExamTimeSlotForm, FilterExamListForm, CandidateBookTimeSlotForm
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

import pdb
import os
import hashlib
import random

##from django.contrib.auth.decorators import permission_required


#def index(request):
#    return HttpResponse("You're at the submit_contributions index.")

#class IndexView(generic.ListView):
#    template_name = 'candidate/index.html'
#    context_object_name = 'candidate_list'

def is_candidate_user(username, request):
    candidate_user = True
    if username.groups.filter(name="Candidate").count() <= 0:
        candidate_user = False
    
    return candidate_user

def is_ra_user(username, request):
    ra_user = True
    if username.groups.filter(name="TNAI").count() <= 0:
        ra_user = False
    
    return ra_user

def exam_list(request):
    username = auth.get_user(request)
    allowed = is_ra_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html',)

    # User is allowed to access page
    queryset = Exam.objects.all()
    # Filter: TODO
#    filter_form = FilterForm()
    return render(request, 'exam/exam_list.html', {'username': username, 'queryset': queryset,}, )

def submit_exam(request):
    username=auth.get_user(request)
    allowed = is_ra_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'TNAI'})

    new_entry = True
    if request.method == 'POST':
        exam_form = ExamForm(request.POST, request.FILES)

        if exam_form.is_valid():
            exam_form.save()
            return HttpResponseRedirect('/exam/exam_list/')
            # if a GET (or any other method) we'll create a blank form
    else:
        if 'exam_id' in request.GET:
            exam_id = request.GET.__getitem__('exam_id')
            new_entry = False
            exam = Exam.objects.get(exam_id=exam_id)
            exam_form = ExamForm(instance=exam)
        else:
            exam_form = ExamForm()

    return render(request, 'exam/submit_exam.html', {'new_entry': new_entry, 'exam_form': exam_form,}) 

def submit_exam_time_slot(request):
    username=auth.get_user(request)
    allowed = is_ra_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'TNAI'})

#    max_snc_per_course = 5
#    total_forms = max_snc_per_course * len(snc_course_choices)
    if request.method == 'GET':
        if 'exam_id' in request.GET:
            exam_id = request.GET.__getitem__('exam_id')
        else:
            return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})
    else:
        if 'exam_id' in request.POST:
            exam_id = request.POST.get('exam_id', "")
        else:
            return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})
    try:
        exam = Exam.objects.get(exam_id=exam_id)
        extra_forms = 1
        ExamTimeSlotFormSet = inlineformset_factory(Exam, ExamTimeSlot, form=ExamTimeSlotForm, extra=extra_forms, can_delete=True)
        qs=ExamTimeSlot.objects.filter(exam=exam).order_by('begin_time')

    except ObjectDoesNotExist:
        return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})

    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        exam_time_slot_formset = ExamTimeSlotFormSet(request.POST, request.FILES, instance=exam, queryset=qs)#, initial={'user': username,})
#        snc_form_instance = StateNursingCouncilForm()
        if exam_time_slot_formset.is_valid():
            exam_time_slot_formset.save()
            return HttpResponseRedirect('/exam/exam_list/')
    else:
        exam_time_slot_formset = ExamTimeSlotFormSet(instance=exam, queryset=qs)

    exam_time_slot_form_instance = exam_time_slot_formset[0]
#    pdb.set_trace()
    return render(request, 'exam/submit_exam_time_slot.html', {'exam_time_slot_formset': exam_time_slot_formset, 'exam_time_slot_form_instance': exam_time_slot_form_instance, 'exam_id': exam_id, })

def candidate_book_time_slot(request):
    username=auth.get_user(request)
    allowed = is_candidate_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'Candidate'})
    candidate = Candidate.objects.get(candidate_username=username)

    exam_id = None
    if request.method == 'GET':
        if 'exam_id' in request.GET:
            exam_id = request.GET.__getitem__('exam_id')
        else:
            return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})
    else:
        if 'exam_id' in request.POST:
            exam_id = request.POST.get('exam_id', "")
        else:
            return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})
    try:
        exam = Exam.objects.get(exam_id=exam_id)
        extra_forms = 1
        ExamTimeSlotFormSet = inlineformset_factory(Exam, ExamTimeSlot, form=ExamTimeSlotForm, extra=extra_forms, can_delete=True)
        qs=ExamTimeSlot.objects.filter(exam=exam).order_by('begin_time')

    except ObjectDoesNotExist:
        return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/candidate/')
        else: # must be "book"
            queryset = ExamTimeSlot.objects.filter(exam_id = exam_id).order_by('begin_time')
            form = CandidateBookTimeSlotForm(request.POST, queryset=queryset)
            pdb.set_trace()
            if form.is_valid():
                time_slot_id = form.cleaned_data['time_slot']
                exam_time_slot = ExamTimeSlot.objects.get(pk=time_slot_id)
                candidate_book_time_slot = CandidateBookTimeSlot()
                candidate_book_time_slot.candidate = candidate
                candidate_book_time_slot.time_slot = exam_time_slot
                candidate_book_time_slot.save()
                return HttpResponseRedirect('/candidate/')
        # check whether it's valid:
        # TODO
#        exam_time_slot_formset = ExamTimeSlotFormSet(request.POST, request.FILES, instance=exam, queryset=qs)#, initial={'user': username,})
#        snc_form_instance = StateNursingCouncilForm()
#        if form.is_valid():
#            form.save()
#            pdb.set_trace()
#            return HttpResponseRedirect('/exam/exam_list/')
    else:
        queryset = ExamTimeSlot.objects.filter(exam_id = exam_id).order_by('begin_time')
        form = CandidateBookTimeSlotForm(queryset=queryset)

    return render(request, 'exam/candidate_book_time_slot.html', {'candidate': candidate, 'exam_id': exam_id, 'exam': exam, 'form': form, })

#def filter_exam_list(request):
#    username=auth.get_user(request)
#    allowed = is_ra_user(username, request) or is_candidate_user(username, request)
#    if not allowed:
#        return render(request, 'exam/not_allowed.html')
#
#    if request.method == 'POST':
#        exam_form = (request.POST, request.FILES)
#
#        if exam_form.is_valid():
#            exam_form.save()
#            return HttpResponseRedirect('/exam/exam_list/')
#            # if a GET (or any other method) we'll create a blank form
#    else:
#        if 'exam_id' in request.GET:
#            exam_id = request.GET.__getitem__('exam_id')
#            new_entry = False
#            exam = Exam.objects.get(exam_id=exam_id)
#            exam_form = ExamForm(instance=exam)
#        else:
#            exam_form = ExamForm()
#
#    return render(request, 'exam/submit_exam.html', {'new_entry': new_entry, 'exam_form': exam_form,}) 
#
