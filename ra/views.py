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
import csv
from django.utils.crypto import get_random_string
from django.contrib import auth
from django.db.models import Q, F, ExpressionWrapper, fields, Sum
from django.db.models.functions import Length

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
from .models import RA, CandidateList
from .forms import ActAsForm, CandidateListForm, ActivateCandidateForm
from .forms import DeleteExamForm, DeleteAdvertisementForm, DeleteUserForm

import pdb

def is_verified_employer(username, request):
    employer_user = True
    verified = True
    if username.groups.filter(name="Employer").count() <= 0:
        employer_user = False

    if employer_user:
        # check verification
        employer = Employer.objects.get(employer_username = username)
        verified = employer.is_employer_verified()
    
    return employer_user and verified

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

def save_candidate_list(name, queryset):
    candidate_list = CandidateList.objects.create(name=name)
    for candidate in queryset:
#        pdb.set_trace()
        candidate_list.members.add(candidate)
    candidate_list.save()
    return candidate_list

def candidate_list(request):
    username = auth.get_user(request)
    verified_employer = is_verified_employer(username, request)
    allowed = is_allowed(username, request) or verified_employer
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    queryset = Candidate.objects.all()
    count = queryset.count()
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

                date_created = filter_form.cleaned_data['date_created']
                if date_created is not None:
                    queryset = queryset.filter(candidate_username__date_joined__date=date_created)

                gender = filter_form.cleaned_data['gender']
                if gender is not None and len(gender) > 0:
                    queryset = queryset.filter(gender=gender)

                professional_qualifications = filter_form.cleaned_data['professional_qualifications']
                if professional_qualifications is not None and len(professional_qualifications) > 0:
                    queryset = queryset.filter(professionalqualifications__class_degree__iexact = professional_qualifications).annotate(institute_name_length=Length('professionalqualifications__institute_name')).filter(institute_name_length__gt=0)

                minimum_experience = filter_form.cleaned_data['minimum_experience']
                if minimum_experience is not None and len(minimum_experience) > 0:
                    duration = ExpressionWrapper(F('experience__date_to') - F('experience__date_from'), output_field=fields.DurationField())
                    queryset = queryset.annotate(experience_duration = duration).annotate(total_experience = Sum('experience_duration'))
                    entered_xp_duration = datetime.timedelta(days = int(minimum_experience) * 30)
                    queryset = queryset.filter(total_experience__gt = entered_xp_duration)

                eligibility_tests = filter_form.cleaned_data['eligibility_tests']
                if eligibility_tests is not None and len(eligibility_tests) > 0:
                    queryset = queryset.filter(eligibilitytests__eligibility_tests__iexact = eligibility_tests).annotate(score_grade_marks_length=Length('eligibilitytests__score_grade_marks')).filter(score_grade_marks_length__gt=0)


                temp = filter_form.cleaned_data['verified']
                if temp is not None and len(temp) > 0:
                    verified = not temp in ['False', 'No']
                    queryset = queryset.filter(is_provisional_registration_number = verified)

                if 'save_candidate_list' in request.POST:
                    name = 'Temporary candidate list: ' + str(timezone.datetime.now())
                    candidate_list = save_candidate_list(name, queryset)
                    return HttpResponseRedirect('/ra/save_list?list_id='+str(candidate_list.list_id))

    else:
        gender = 'Any'
        experience = ''
        eligibility_tests = ''
        try:
            gender = request.GET.__getitem__('gender')
            experience = request.GET.__getitem__('experience')
            eligibility_tests = request.GET.__getitem__('eligibility_tests')
        except KeyError:
            pass
        filter_form = FilterForm(initial = {'gender': gender, 'minimum_experience': experience, 'eligibility_tests': eligibility_tests})

    if verified_employer:
        queryset = queryset.filter(is_provisional_registration_number = False)
        count = queryset.count()
    return render(request, 'ra/candidate_list.html', {'queryset': queryset, 'filter_form': filter_form, 'count': count, 'verified_employer': verified_employer, }, )

def filter_candidates(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    if request.method == 'GET':
        try:
            advertisement_id = request.GET.__getitem__('advertisement_id')
            advertisement = Advertisement.objects.get(obfuscated_id = advertisement_id)
            gender = advertisement.gender
            experience = advertisement.experience
            eligibility_tests = advertisement.eligibility_tests
            return HttpResponseRedirect('/ra/candidate_list/?gender=' + gender + '&experience=' + experience + '&eligibility_tests=' + eligibility_tests + '#filter')
        except KeyError:
            return render(request, 'home/error_msg.html', {'error_msg': 'Missing advertisement ID'})
        except ObjectDoesNotExist:
            return render(request, 'home/error_msg.html', {'error_msg': 'Invalid advertisement ID: ' + advertisement_id})
    else:
        return HttpResponseRedirect('/ra/')

def generate_list_of_exam_candidates(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

def manipulate_list(request):
    pass

def show_saved_candidate_lists(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    queryset = CandidateList.objects.all()
    return render(request, 'ra/show_saved_candidate_lists.html', {'queryset': queryset})

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

def list_of_candidates_list(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    queryset = CandidateList.objects.all()
    return render(request, 'ra/list_of_candidates_list.html', {'queryset': queryset}, )

def save_list(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    # User is allowed to access page
    if request.method == 'POST':
        try:
            list_id = request.POST.get('list_id')
        except KeyError:
            return render(request, 'ra/invalid_list_id.html', {'list_id': None }, )
        try:
            candidate_list = CandidateList.objects.get(list_id=list_id)
        except ObjectDoesNotExist:
            return render(request, 'ra/invalid_list_id.html', {'list_id': None }, )

        form = CandidateListForm(request.POST, instance = candidate_list)
        if form.is_valid():
            if 'update' in request.POST:
                form.save()
            elif 'discard' in request.POST:
                candidate_list.delete()
            elif 'send_email' in request.POST:
                current_site = get_current_site(request)
#                user = candidate.candidate_username
                message = form.cleaned_data['notes']
#                message = render_to_string('candidate/provisional_registration_number_email.html', {
#                    'user':user, 
#                    'domain':current_site.domain,
#                    'registration_number_display': candidate.registration_number_display()
#                })
                mail_subject = 'Notification from TNAI'
                attachment = None
                if len(request.FILES) > 0:
                    attachment = request.FILES['attachment']
                    attachment_name = attachment.name
                    attachment_data = attachment.read()
                    attachment_content_type = attachment.content_type

                for candidate in candidate_list.members.all():
                    to_email = candidate.candidate_username.username
                    email = EmailMessage(mail_subject, message, to=[to_email])
#                    pdb.set_trace()
                    if attachment is not None:
                        email.attach(attachment_name, attachment_data, attachment_content_type)
                    result = email.send()
                form.save()
            elif 'export_csv' in request.POST:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="candidate-list-"' + str(list_id) + '.csv"'

                writer = csv.writer(response)
                writer.writerow(['Username', 'Name'])
                for candidate in candidate_list.members.all():
                    candidate_username = candidate.candidate_username.username
                    candidate_name = candidate.name
                    writer.writerow([candidate_username, candidate_name])
                return response
            elif 'do_nothing' in request.POST:
                pass
            return HttpResponseRedirect('/ra/')
    else:
        try:
            list_id = request.GET.__getitem__('list_id')
        except KeyError:
            return render(request, 'ra/invalid_list_id.html', {'list_id': None }, )
        try:
            candidate_list = CandidateList.objects.get(list_id=list_id)
        except ObjectDoesNotExist:
            return render(request, 'ra/invalid_list_id.html', {'list_id': list_id }, )

        form = CandidateListForm(instance = candidate_list)

    return render(request, 'ra/save_list.html', {'form': form, 'candidate_list': candidate_list, }, )

def manipulate_candidate_list(request):
    pass

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
        elif 'verify_no' in request.POST:
            registration_number = request.POST.get('registration_number')
            candidate = Candidate.objects.get(registration_number=registration_number)
            candidate.is_provisional_registration_number = True
            candidate.save()
            return HttpResponseRedirect('/candidate/candidate_profile?registration_number='+str(registration_number))
        else:
            return HttpResponseRedirect('/ra/')

def verify_employer(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)

    if request.method == 'GET':
        registration_number = request.GET.__getitem__('registration_number')
        try:
            employer = Employer.objects.get(registration_number=registration_number)
        except ObjectDoesNotExist:
            return render(request, 'ra/invalid_registration_number.html', {'registration_number': registration_number}, )

        return render(request, 'ra/verify_employer.html', {'employer': employer}, )
    else:
        if 'verify_yes' in request.POST:
            registration_number = request.POST.get('registration_number')
            employer = Employer.objects.get(registration_number=registration_number)
            employer.is_provisional_registration_number = False
            employer.save()
            return HttpResponseRedirect('/employer/entire_profile?registration_number='+str(registration_number))
        elif 'verify_no' in request.POST:
            registration_number = request.POST.get('registration_number')
            employer = Employer.objects.get(registration_number=registration_number)
            employer.is_provisional_registration_number = True
            employer.save()
            return HttpResponseRedirect('/employer/entire_profile?registration_number='+str(registration_number))
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
        try:
            acting_as_username = request.GET.__getitem__('acting_as_username')
            acting_as = User.objects.get(username=acting_as_username)
            ra.acting_as = acting_as
        except KeyError:
            pass
        form = ActAsForm(instance=ra)

    return render(request, 'ra/act_as.html', {'form': form, 'next': next}, )

def activate_candidate(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)
    ra = RA.objects.get(logged_in_as=username)

    if request.method == 'POST':
        form = ActivateCandidateForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if not user.is_active:
                user.is_active = True
                user.save()
                g = Group.objects.get(name='Candidate') 
                g.user_set.add(user)
            else:
                return render(request, 'ra/username_already_activated.html', {'username': user.username }, )
            return HttpResponseRedirect('/ra/')
    else:
        form = ActivateCandidateForm()

    return render(request, 'ra/activate_candidate.html', {'form': form, 'next': next}, )

def delete_user(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)
    ra = RA.objects.get(logged_in_as=username)

    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            username_to_be_deleted = form.cleaned_data['username']
            try:
                user_to_be_deleted = User.objects.get(username = username_to_be_deleted)
                user_to_be_deleted.delete()
            except ObjectDoesNotExist:
                return render(request, 'ra/invalid_username.html', {'username': username_to_be_deleted }, )
            return HttpResponseRedirect('/ra/')
    else:
        form = DeleteUserForm()

    return render(request, 'ra/delete_advertisement.html', {'form': form, 'next': next}, )

def delete_advertisement(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)
    ra = RA.objects.get(logged_in_as=username)

    if request.method == 'POST':
        form = DeleteAdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.cleaned_data['advertisement']
            advertisement.delete()
            return HttpResponseRedirect('/ra/')
    else:
        form = DeleteAdvertisementForm()

    return render(request, 'ra/delete_advertisement.html', {'form': form, 'next': next}, )

def delete_exam(request):
    username = auth.get_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'ra/not_allowed.html',)
    ra = RA.objects.get(logged_in_as=username)

    if request.method == 'POST':
        form = DeleteExamForm(request.POST)
        if form.is_valid():
            exam = form.cleaned_data['exam']
            exam.delete()
            return HttpResponseRedirect('/ra/')
    else:
        form = DeleteExamForm()

    return render(request, 'ra/delete_exam.html', {'form': form, 'next': next}, )
