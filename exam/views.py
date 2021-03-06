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
from .forms import ExamForm, ExamTimeSlotForm, FilterExamListForm, CandidateBookTimeSlotForm, ShowInterestInExamForm
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

from ra.models import RA, CandidateList

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

def get_acting_user(request):
    username=auth.get_user(request)
    if is_ra_user(username, request):
        ra = RA.objects.get(logged_in_as=username)
        if ra.acting_as is not None:
            username = ra.acting_as

    return username

def get_exam_from_request(request):
    if request.method == 'GET':
        try:
            exam_id = request.GET.__getitem__('exam_id')
        except KeyError:
            error_msg = "Exam ID not specified."
            return (None, None, HttpResponseRedirect("/home/error_msg?error_msg="+ error_msg))

        try:
            exam = Exam.objects.get(exam_id = exam_id)
        except ObjectDoesNotExist:
            error_msg = "Exam ID: " + str(exam_id) + " invalid."
            return (exam_id, None, HttpResponseRedirect("/home/error_msg?error_msg="+ error_msg))
    else:
        try:
            exam_id = request.POST.get('exam_id')
        except KeyError:
            error_msg = "Exam ID not specified."
            return (None, None, HttpResponseRedirect("/home/error_msg?error_msg=" + error_msg))

        try:
            exam = Exam.objects.get(exam_id = exam_id)
        except ObjectDoesNotExist:
            error_msg = "Exam ID: " + str(exam_id) + " invalid."
            return (exam_id, None, HttpResponseRedirect("/home/error_msg?error_msg=" + error_msg))

    return (exam_id, exam, None)

def show_exam_details(request):
    username = get_acting_user(request)
    candidate_user_type = is_candidate_user(username, request)
    ra_user_type = is_ra_user(username, request)
    allowed = candidate_user_type or ra_user_type
    error_msg = ""
    if candidate_user_type:
        candidate = Candidate.objects.get(candidate_username = username)
#        allowed = candidate.is_candidate_verified()
        if not allowed:
            error_msg = "Candidate not verified."

    if not allowed:
        return render(request, 'exam/not_allowed.html', {'error_msg': error_msg})

    exam_id = None
    interested = False

    if request.method == 'GET':
        try:
            exam_id = request.GET.__getitem__('exam_id')
        except KeyError:
            error_msg = "Exam ID not specified."
            return HttpResponseRedirect("/home/error_msg?error_msg="+ error_msg)

        try:
            exam = Exam.objects.get(exam_id = exam_id)
        except ObjectDoesNotExist:
            error_msg = "Exam ID: " + str(exam_id) + " invalid."
            return HttpResponseRedirect("/home/error_msg?error_msg="+ error_msg)

        if candidate_user_type:
            (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Showed interest", defaults = {'name': str(exam) + " interested candidates list", 'time_created': timezone.now(), })
            candidate = Candidate.objects.get(candidate_username = username)
            candidate_is_member_of_candidate_list = candidate_list in candidate.candidatelist_set.all()
            if candidate_is_member_of_candidate_list:
                form = ShowInterestInExamForm(initial = {'interested': True})
            else:
                form = ShowInterestInExamForm(initial = {'interested': False})
        else:
            form = ShowInterestInExamForm()
    else:
        try:
            exam_id = request.POST.get('exam_id')
        except KeyError:
            error_msg = "Exam ID not specified."
            return HttpResponseRedirect("/home/error_msg?error_msg=" + error_msg)

        try:
            exam = Exam.objects.get(exam_id = exam_id)
        except ObjectDoesNotExist:
            error_msg = "Exam ID: " + str(exam_id) + " invalid."
            return HttpResponseRedirect("/home/error_msg?error_msg=" + error_msg)

        form = ShowInterestInExamForm(request.POST)
        if form.is_valid():
            if candidate_user_type and 'update_interest' in request.POST:
                interested = form.cleaned_data['interested']
                if interested:
                    (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Showed interest", defaults = {'name': str(exam) + " interested candidates list", 'time_created': timezone.now(), })
                    candidate = Candidate.objects.get(candidate_username = username)
                    candidate_list.members.add(candidate)
                    candidate_list.save()
                    return HttpResponseRedirect("/home/success_msg/?success_msg=Successfully added to 'Interested' list for Exam ID: " + str(exam.exam_id))
                else:
                    (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Showed interest", defaults = {'name': str(exam) + " interested candidates list", 'time_created': timezone.now(), })
                    candidate = Candidate.objects.get(candidate_username = username)
                    candidate_list.members.remove(candidate)
                    candidate_list.save()
                    return HttpResponseRedirect("/home/success_msg/?success_msg=Successfully removed from 'Interested' list for Exam ID:" + str(exam.exam_id))
            else:
                return HttpResponseRedirect('/')
    return render(request, 'exam/show_exam_details.html', {'exam': exam, 'interested': interested, 'candidate_user_type': candidate_user_type, 'form': form, })

def exam_list(request):
    username = get_acting_user(request)
    candidate_user_type = is_candidate_user(username, request)
    ra_user_type = is_ra_user(username, request)
    allowed = candidate_user_type or ra_user_type
    error_msg = ""
    if candidate_user_type:
        candidate = Candidate.objects.get(candidate_username = username)
#        allowed = candidate.is_candidate_verified()
        if not allowed:
            error_msg = "Candidate not verified."

    if not allowed:
        return render(request, 'exam/not_allowed.html', {'error_msg': error_msg})

    # User is allowed to access page
    queryset = Exam.objects.all().order_by('date')
    # Filter: TODO
    if request.method == 'POST':
        if 'clear_all_filters' in request.POST:
            filter_form = FilterExamListForm()
        else:
            filter_form = FilterExamListForm(request.POST)
            if filter_form.is_valid():
                exam_name = filter_form.cleaned_data['exam_name']
                if exam_name is not None and len(exam_name) > 0:
                    queryset = queryset.filter(name__icontains=exam_name)

                exam_date = filter_form.cleaned_data['exam_date']
                if exam_date is not None:
                    queryset = queryset.filter(date=exam_date)

                exam_type = filter_form.cleaned_data['exam_type']
                if exam_type is not None and len(exam_type) > 0:
                    queryset = queryset.filter(exam_type=exam_type)

#                only_show_interesting = filter_form.cleaned_data['only_show_interesting']
#                # TODO
                if candidate_user_type:
                    queryset = queryset.filter(candidatelist__members = candidate)
    else:
        filter_form = FilterExamListForm()

    return render(request, 'exam/exam_list.html', {'username': username, 'queryset': queryset, 'filter_form': filter_form, 'candidate_user_type': candidate_user_type, 'ra_user_type': ra_user_type, })

def submit_exam(request):
    username = get_acting_user(request)
    allowed = is_ra_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'TNAI'})

    new_entry = True
    if request.method == 'POST':
        if 'exam_id' in request.POST:
            exam_id = request.POST.get('exam_id')
        else:
            exam_id = ""
        if len(exam_id) > 0:
            exam = Exam.objects.get(exam_id = exam_id)
            exam_form = ExamForm(request.POST, request.FILES, instance = exam)
        else:
            exam_form = ExamForm(request.POST, request.FILES)

        if exam_form.is_valid():
            exam = exam_form.save()
            return HttpResponseRedirect('/exam/exam_list/')
            # if a GET (or any other method) we'll create a blank form
    else:
        if 'exam_id' in request.GET:
            exam_id = request.GET.__getitem__('exam_id')
            new_entry = False
            exam = Exam.objects.get(exam_id=exam_id)
            exam_form = ExamForm(instance=exam)
        else:
            exam_id = ""
            exam_form = ExamForm()

    return render(request, 'exam/submit_exam.html', {'new_entry': new_entry, 'exam_form': exam_form, 'exam_id': exam_id, }) 

def submit_exam_time_slot(request):
    username = get_acting_user(request)
    allowed = is_ra_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'TNAI'})

#    max_snc_per_course = 5
#    total_forms = max_snc_per_course * len(snc_course_choices)
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
        # check whether it's valid:
        # TODO
        exam_time_slot_formset = ExamTimeSlotFormSet(request.POST, request.FILES, instance=exam, queryset=qs)#, initial={'user': username,})
#        snc_form_instance = StateNursingCouncilForm()
#        pdb.set_trace()
        if exam_time_slot_formset.is_valid():
            exam_time_slot_formset.save()
            return HttpResponseRedirect('/exam/exam_list/')
    else:
        exam_time_slot_formset = ExamTimeSlotFormSet(instance=exam, queryset=qs)

    exam_time_slot_form_instance = exam_time_slot_formset[0]
#    pdb.set_trace()
    return render(request, 'exam/submit_exam_time_slot.html', {'exam_time_slot_formset': exam_time_slot_formset, 'exam_time_slot_form_instance': exam_time_slot_form_instance, 'exam_id': exam_id, })

def candidate_download_hall_ticket(request):
    username = get_acting_user(request)
    allowed = is_candidate_user(username, request)
    error_msg = "Not a registered candidate"
    if allowed:
        # Add a verification check
        candidate = Candidate.objects.get(candidate_username=username)
        displayed_registration_number = candidate.registration_number_display()
#        allowed = candidate.is_candidate_verified()
        if not allowed:
            error_msg = "Candidate not verified."

    if not allowed:
        return HttpResponseRedirect('/home/error_msg/?error_msg=' + error_msg)

    if request.method == 'GET':
        if 'exam_id' in request.GET:
            exam_id = request.GET.__getitem__('exam_id')
        else:
            return HttpResponseRedirect('/home/error_msg/?error_msg=' + "Required parameter 'Exam ID' not found.")

        try:
            exam = Exam.objects.get(exam_id = exam_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/home/error_msg/?error_msg=' + "Exam ID: " + str(exam_id) + " is invalid.")

        (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Downloaded hall ticket", defaults = {'name': str(exam) + " list of candidates who dowloaded hall tickets", })
        if candidate in candidate_list.members.all():
            return HttpResponseRedirect('/exam/candidate_show_hall_ticket/?exam_id=' + exam_id)

    else:
        if 'exam_id' in request.POST:
            exam_id = request.POST.get('exam_id')
        else:
            return HttpResponseRedirect('/home/error_msg/?error_msg=' + "Required parameter 'Exam ID' not found.")
        try:
            exam = Exam.objects.get(exam_id = exam_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/home/error_msg/?error_msg=' + "Exam ID: " + str(exam_id) + " is invalid.")

        if 'download' in request.POST:
            (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Downloaded hall ticket", defaults = {'name': str(exam) + " list of candidates who dowloaded hall tickets", })
            candidate_list.members.add(candidate)
            return HttpResponseRedirect('/exam/candidate_show_hall_ticket/?exam_id=' + exam_id)
        else:
            return HttpResponseRedirect('/candidate/')

    return render(request, 'exam/candidate_download_hall_ticket.html', {'exam': exam, 'candidate': candidate, 'displayed_registration_number': displayed_registration_number, })

def candidate_show_hall_ticket(request):
    username = get_acting_user(request)
    allowed = is_candidate_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'Candidate'})
    candidate = Candidate.objects.get(candidate_username=username)
    displayed_registration_number = candidate.registration_number_display()

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

    except ObjectDoesNotExist:
        return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id})

    try:
        booking = CandidateBookTimeSlot.objects.filter(candidate=candidate).get(exam=exam)
    except ObjectDoesNotExist:
        return render(request, 'exam/booking_does_not_exist.html', {'exam_id': exam_id})

    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'exam/candidate_show_hall_ticket.html', {'candidate': candidate, 'displayed_registration_number': displayed_registration_number, 'exam_id': exam_id, 'exam': exam, 'booking': booking, })

def candidate_book_time_slot(request):
    username = get_acting_user(request)
    allowed = is_candidate_user(username, request)
    if not allowed:
        return render(request, 'exam/not_allowed.html', {'not_member_of_group': 'Candidate'})
    candidate = Candidate.objects.get(candidate_username=username)

    candidate_list = CandidateList.objects.get(exam = exam, exam_list_type = "Downloaded hall ticket")
    if candidate in candidate_list.members.all():
        error_msg = "Hall ticket already downloaded. Exam time slot cannot be changed."
        return (None, None, HttpResponseRedirect("/home/error_msg?error_msg="+ error_msg))

    exam_id = None
    booking = None
    if request.method == 'GET':
        if 'exam_id' in request.GET:
            exam_id = request.GET.__getitem__('exam_id')
        else:
            return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id, })
    else:
        if 'exam_id' in request.POST:
            exam_id = request.POST.get('exam_id', "")
        else:
            return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id, })
    try:
        exam = Exam.objects.get(exam_id=exam_id)
        extra_forms = 1
        ExamTimeSlotFormSet = inlineformset_factory(Exam, ExamTimeSlot, form=ExamTimeSlotForm, extra=extra_forms, can_delete=True)
        qs=ExamTimeSlot.objects.filter(exam=exam).order_by('begin_time')

    except ObjectDoesNotExist:
        return render(request, 'exam/exam_id_not_found.html', {'exam_id': exam_id, })

    try:
        booking = CandidateBookTimeSlot.objects.filter(candidate=candidate).get(exam=exam)
        if booking.hall_ticket_downloaded:
            return render(request, 'exam/hall_ticket_already_downloaded.html')
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        if booking is not None:
            booking.delete() # cancel old booking
            (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Booked time slot", defaults = {'name': str(exam) + " candidates who have booked time slots", })
        if 'cancel_booking' in request.POST:
            return HttpResponseRedirect('/candidate/booked_exam_time_slots/')
        else: # must be "book"
            queryset = ExamTimeSlot.objects.filter(exam_id = exam_id).order_by('begin_time')
            form = CandidateBookTimeSlotForm(request.POST, queryset=queryset)
            if form.is_valid():
                time_slot_id = form.cleaned_data['time_slot']
                exam_time_slot = ExamTimeSlot.objects.get(pk=time_slot_id)
                candidate_book_time_slot = CandidateBookTimeSlot()
                candidate_book_time_slot.candidate = candidate
                candidate_book_time_slot.exam = exam
                candidate_book_time_slot.time_slot = exam_time_slot
                candidate_book_time_slot.save()
                (candidate_list, created) = CandidateList.objects.get_or_create(exam = exam, exam_list_type = "Booked time slot", defaults = {'name': str(exam) + " candidates who have booked time slots", })
                candidate_list.members.add(candidate)
                candidate_list.save()
                return HttpResponseRedirect('/candidate/booked_exam_time_slots/')
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
        try:
            booking = CandidateBookTimeSlot.objects.filter(candidate=candidate).get(exam=exam)
            form = CandidateBookTimeSlotForm(queryset = queryset, booked_time_slot = booking.time_slot)
        except ObjectDoesNotExist:
            booked_time_slot = None
            form = CandidateBookTimeSlotForm(queryset = queryset)

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
