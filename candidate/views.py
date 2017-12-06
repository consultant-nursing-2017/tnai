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
from .models import Candidate, EducationalQualifications, ProfessionalQualifications, AdditionalQualifications, EligibilityTests, Experience, StateNursingCouncil, StateNursingCouncilName
from .forms import SubmitForm, PersonalForm, StateNursingCouncilForm, EducationalQualificationsForm, ProfessionalQualificationsForm, AdditionalQualificationsForm, EligibilityTestsForm, ExperienceForm, PassportAndMiscForm, StateNursingCouncilForm, CandidateFindJobsForm
from employer.models import Employer, Advertisement
from exam.models import ExamTimeSlot, CandidateBookTimeSlot
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
from ra.models import RA

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

def is_employer_user(username, request):
    employer_user = True
    if username.groups.filter(name="Employer").count() <= 0:
        employer_user = False
    
    return employer_user

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

def is_allowed(username, request):
    allowed = True
    if not is_candidate_user(username, request) and not is_ra_user(username, request):
        allowed = False
    
    return allowed

def get_acting_user(request):
    username=auth.get_user(request)
    if is_ra_user(username, request):
        try:
            ra = RA.objects.get(logged_in_as=username)
            if ra.acting_as is not None:
                username = ra.acting_as
        except ObjectDoesNotExist:
            pass

    return username

def redirect_to_tab(request):
    if 'save_personal' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')
    elif 'save_educational' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_educational_qualifications/')
    elif 'save_professional' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_professional_qualifications/')
    elif 'save_additional' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_additional_qualifications/')
    elif 'save_experience' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_experience/')
    elif 'save_eligibility' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_eligibility_tests/')
    elif 'save_state_nursing_council' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_snc/')
    elif 'save_passport' in request.POST:
        return HttpResponseRedirect('/candidate/submit_candidate_passport/')
    else:
        return HttpResponseRedirect('/candidate/candidate_profile/')

def candidate_index(request):
    actual_user = auth.get_user(request)
    username = get_acting_user(request)
    if is_employer_user(username, request):
        return HttpResponseRedirect('/employer/')
    elif is_ra_user(username, request) and username == actual_user:
        return HttpResponseRedirect('/ra/')

    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    object_does_not_exist = False
    try:
        if username.is_authenticated():
            candidate = Candidate.objects.get(candidate_username=username)
        else:
            candidate = None
    except ObjectDoesNotExist:
        candidate = None
        object_does_not_exist = True

    displayed_registration_number = None
    if candidate.registration_number is not None:
        displayed_registration_number = candidate.registration_number_display()
    return render(request, 'candidate/index.html', {'candidate': candidate, 'object_does_not_exist': object_does_not_exist, 'displayed_registration_number': displayed_registration_number, }) 

def submit_candidate_personal(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    new_profile = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            candidate = Candidate.objects.get(candidate_username=username)
            new_profile = False
            personal_form = PersonalForm(request.POST, request.FILES, instance=candidate)
#            candidate = Candidate.objects.get(candidate_username=username)
        except ObjectDoesNotExist:
            new_profile = True
            personal_form = PersonalForm(request.POST, request.FILES)

        if personal_form.is_valid():
            personal_form.save()
            return redirect_to_tab(request)
            # if a GET (or any other method) we'll create a blank form
    else:
        try:
            candidate = Candidate.objects.get(candidate_username=username)
            personal_form = PersonalForm(instance=candidate)
            new_profile = False
        except ObjectDoesNotExist:
            new_profile = True
            personal_form = PersonalForm(initial={'candidate_username': username,})

    return render(request, 'candidate/submit_candidate_personal.html', {'new_profile': new_profile, 'personal_form': personal_form,}) 

def submit_candidate_educational_qualifications(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    new_profile = False
    error_message = ""
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        educational_qualifications_queryset = EducationalQualifications.objects.filter(candidate=candidate)
#        educational_qualifictions_queryset = [p for p in educational_queryset if not hasattr(p, 'professionalqualifications')]
        num_educational_qualifications = educational_qualifications_queryset.count()
        if num_educational_qualifications > 3:
            raise ValidationError(_('num_educational_qualifications is greater than 3, value: %(value)s'), params={'value': 'num_educational_qualifications'},)
        extra_forms = 3 - num_educational_qualifications
        EducationalQualificationsFormSet = inlineformset_factory(Candidate, EducationalQualifications, form=EducationalQualificationsForm, extra=extra_forms, can_delete=False)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')
    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        educational_qualifications_formset = EducationalQualificationsFormSet(request.POST, request.FILES, instance=candidate, queryset=educational_qualifications_queryset)#, initial={'user': username,})
#        educational_qualifications_form_instance = EducationalQualificationsForm()
#        pdb.set_trace()
        if educational_qualifications_formset.is_valid():
            educational_qualifications_formset.save()
            return redirect_to_tab(request)

    else:
        if num_educational_qualifications > 0:
            educational_qualifications_formset = EducationalQualificationsFormSet(instance=candidate, queryset=educational_qualifications_queryset)
        else:
            educational_qualifications_formset = EducationalQualificationsFormSet(instance=candidate,
                initial=[{'class_degree': '10th'}, {'class_degree': '12th/Equivalent'}], queryset=educational_qualifications_queryset)

    educational_qualifications_form_instance = educational_qualifications_formset[0]
    return render(request, 'candidate/submit_candidate_educational_qualifications.html', {'educational_qualifications_formset': educational_qualifications_formset, 'educational_qualifications_form_instance': educational_qualifications_form_instance, 'error_message': error_message})

def submit_candidate_professional_qualifications(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    new_profile = False
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        num_professional_qualifications = ProfessionalQualifications.objects.filter(candidate=candidate).count()
        if num_professional_qualifications > 5:
            raise ValidationError(_('num_professional_qualifications is greater than 5, value: %(value)s'), params={'value': 'num_professional_qualifications'},)
        extra_forms = 5 - num_professional_qualifications
        ProfessionalQualificationsFormSet = inlineformset_factory(Candidate, ProfessionalQualifications, form=ProfessionalQualificationsForm, extra=extra_forms, can_delete=False)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')
    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        professional_qualifications_formset = ProfessionalQualificationsFormSet(request.POST, request.FILES, instance=candidate)#, initial={'user': username,})
#        professional_qualifications_form_instance = ProfessionalQualificationsForm()
        if professional_qualifications_formset.is_valid():
            professional_qualifications_formset.save()
            return redirect_to_tab(request)
    else:
        if num_professional_qualifications > 0:
            professional_qualifications_formset = ProfessionalQualificationsFormSet(instance=candidate)#, initial={'user': username,})
        else:
            courses = ProfessionalQualifications.course_choices()
            initial_courses = []
            for course in courses:
                initial_courses.append({'class_degree': course})
            professional_qualifications_formset = ProfessionalQualificationsFormSet(instance=candidate,
                initial=initial_courses) #, initial={'user': username,})

    professional_qualifications_form_instance = professional_qualifications_formset[0]
    return render(request, 'candidate/submit_candidate_professional_qualifications.html', {'professional_qualifications_formset': professional_qualifications_formset, 'professional_qualifications_form_instance': professional_qualifications_form_instance, })

def submit_candidate_additional_qualifications(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    new_profile = False
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        num_additional_qualifications = AdditionalQualifications.objects.filter(candidate=candidate).count()
        if num_additional_qualifications > 5:
            raise ValidationError(_('num_additional_qualifications is greater than 5, value: %(value)s'), params={'value': 'num_additional_qualifications'},)
        extra_forms = 5 - num_additional_qualifications
        AdditionalQualificationsFormSet = inlineformset_factory(Candidate, AdditionalQualifications, form=AdditionalQualificationsForm, extra=extra_forms, can_delete=False)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')
    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        additional_qualifications_formset = AdditionalQualificationsFormSet(request.POST, request.FILES, instance=candidate)#, initial={'user': username,})
#        additional_qualifications_form_instance = AdditionalQualificationsForm()
        if additional_qualifications_formset.is_valid():
            additional_qualifications_formset.save()
            return redirect_to_tab(request)
    else:
#        if num_additional_qualifications > 0:
        additional_qualifications_formset = AdditionalQualificationsFormSet(instance=candidate)#, initial={'user': username,})
#        else:
#            additional_qualifications_formset = AdditionalQualificationsFormSet(instance=candidate,
#                initial=[{'class_degree': 'ANM'}, {'class_degree': 'GNM'}, {'class_degree': 'B. Sc.(N)'}, {'class_degree': 'P. B. B. Sc.(N)'}, {'class_degree': 'M. Sc.(N)'},]) #, initial={'user': username,})

    additional_qualifications_form_instance = additional_qualifications_formset[0]
    return render(request, 'candidate/submit_candidate_additional_qualifications.html', {'additional_qualifications_formset': additional_qualifications_formset, 'additional_qualifications_form_instance': additional_qualifications_form_instance, })

def submit_candidate_experience(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    new_profile = False
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        num_experience = Experience.objects.filter(candidate=candidate).count()
        if num_experience > 10:
            raise ValidationError(_('num_experience is greater than 10, value: %(value)s'), params={'value': 'num_experience'},)
        extra_forms = 10 - num_experience
        ExperienceFormSet = inlineformset_factory(Candidate, Experience, form=ExperienceForm, extra=extra_forms, can_delete=False)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')
    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        experience_formset = ExperienceFormSet(request.POST, request.FILES, instance=candidate)#, initial={'user': username,})
#        experience_form_instance = ExperienceForm()
        if experience_formset.is_valid():
            experience_formset.save()
            return redirect_to_tab(request)
    else:
        experience_formset = ExperienceFormSet(instance=candidate,) #, initial={'user': username,})

    experience_form_instance = experience_formset[0]
    return render(request, 'candidate/submit_candidate_experience.html', {'experience_formset': experience_formset, 'experience_form_instance': experience_form_instance, })

def submit_candidate_eligibility_tests(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    try:
        candidate = Candidate.objects.get(candidate_username=username)
        num_eligibility_tests = EligibilityTests.objects.filter(candidate=candidate).count()
        num_total_elibility_tests_choices = EligibilityTests.eligibility_tests_choices()
        total_choices = len(num_total_elibility_tests_choices)
        if num_eligibility_tests > total_choices:
            raise ValidationError(_('num_eligibility_tests is greater than %(total_choices), value: %(value)s'), params={'value': 'num_eligibility_tests', 'total_choices': 'total_choices'},)
        extra_forms = total_choices - num_eligibility_tests
        EligibilityTestsFormSet = inlineformset_factory(Candidate, EligibilityTests, form=EligibilityTestsForm, extra=extra_forms, can_delete=False)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')

    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        eligibility_tests_formset = EligibilityTestsFormSet(request.POST, request.FILES, instance=candidate)#, initial={'user': username,})
#        eligibility_tests_form_instance = EligibilityTestsForm()
        if eligibility_tests_formset.is_valid():
            eligibility_tests_formset.save()
            return redirect_to_tab(request)
    else:
        if num_eligibility_tests > 0:
            eligibility_tests_formset = EligibilityTestsFormSet(instance=candidate)#, initial={'user': username,})
        else:
            eligibility_tests_formset = EligibilityTestsFormSet(instance=candidate,
                initial=[{'eligibility_tests': 'Prometric (Saudi Arabia)'}, {'eligibility_tests': 'Prometric (UAE)'}, {'eligibility_tests': 'Prometric (Qatar)'}, {'eligibility_tests': 'HAAD'}, {'eligibility_tests': 'DHA'}, {'eligibility_tests': 'IELTS'}, {'eligibility_tests': 'CGFNS'}, {'eligibility_tests': 'TOEFL'}, {'eligibility_tests': 'OET'},]) #, initial={'user': username,})

#        eligibility_tests_form_instance = EligibilityTestsForm()

    eligibility_tests_form_instance = eligibility_tests_formset[0]
    return render(request, 'candidate/submit_candidate_eligibility_tests.html', {'eligibility_tests_formset': eligibility_tests_formset, 'eligibility_tests_form_instance': eligibility_tests_form_instance, })

def submit_candidate_passport(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    try:
        candidate = Candidate.objects.get(candidate_username=username)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')

    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        passport_form = PassportAndMiscForm(request.POST, request.FILES, instance=candidate)
        if passport_form.is_valid():
            passport_form.save()
            return redirect_to_tab(request)
            # if a GET (or any other method) we'll create a blank form
    else:
        passport_form = PassportAndMiscForm(instance=candidate)

    return render(request, 'candidate/submit_candidate_passport.html', {'passport_form': passport_form,}) 

def submit_candidate_snc(request):
    username=get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    snc_course_choices = StateNursingCouncil.course_choices()
    max_snc_per_course = 5
    total_forms = max_snc_per_course * len(snc_course_choices)
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        num_snc = StateNursingCouncil.objects.filter(candidate=candidate).count()
        if num_snc > total_forms:
            raise ValidationError(_('num_snc is greater than %(total_forms), value: %(value)s'), params={'value': 'num_snc', 'total_forms': 'total_forms', },)
        extra_forms = 1
        StateNursingCouncilFormSet = inlineformset_factory(Candidate, StateNursingCouncil, form=StateNursingCouncilForm, extra=extra_forms, can_delete=False)
        qs=StateNursingCouncil.objects.filter(candidate=candidate).order_by('course')

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')

    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        snc_formset = StateNursingCouncilFormSet(request.POST, request.FILES, instance=candidate, queryset=qs)#, initial={'user': username,})
#        snc_form_instance = StateNursingCouncilForm()
        if snc_formset.is_valid():
            snc_formset.save()
            return redirect_to_tab(request)
    else:
        snc_formset = StateNursingCouncilFormSet(instance=candidate, queryset=qs)

    snc_form_instance = snc_formset[0]
#    pdb.set_trace()
    return render(request, 'candidate/submit_candidate_snc.html', {'snc_formset': snc_formset, 'snc_form_instance': snc_form_instance, 'snc_course_choices': snc_course_choices, 'total_forms': total_forms, 'max_snc_per_course': max_snc_per_course, })

def entire_profile(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    updation_allowed = is_candidate_user(username, request)
    ra_user = is_ra_user(username, request)
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    try:
        if 'registration_number' in request.GET:
            registration_number = request.GET.__getitem__('registration_number')
            candidate = Candidate.objects.get(registration_number=registration_number)
            if not is_ra_user(username, request) and candidate.candidate_username != username:
                return render(request, 'candidate/not_allowed.html', {'next': request.path}, )
        else:
            candidate = Candidate.objects.get(candidate_username=username)
        personal_data = [['Name', 'name'], ['Father\'s Name', 'fathers_name'], ['Date of Birth', 'date_of_birth'], ['Gender', 'gender'], ['Marital Status', 'marital_status'], ['Phone Number', 'phone_number'], ]
        for i, field in enumerate(personal_data):
            personal_data[i].append(getattr(candidate, field[1]))

        address_data = [['House Number', 'house_number'], ['Area', 'area_locality'], ['Street', 'street_name'], ['Village', 'village_PS_PO'], ['Country', 'country'], ['State', 'state'], ['City', 'city'], ['District', 'district'], ['Pin Code', 'pin_code']]
        for i, field in enumerate(address_data):
            address_data[i].append(getattr(candidate, field[1]))

        passport_misc_data = [['Passport number', 'passport_number'], ['Passport valid from', 'passport_valid_from'], ['Passport valid to', 'passport_valid_to'], ['Passport place of issue', 'passport_place_of_issue'], ['TNAI number', 'TNAI_number'], ['Preference of work', 'preference_of_work']]
        for i, field in enumerate(passport_misc_data):
            passport_misc_data[i].append(getattr(candidate, field[1]))
#        if len(passport_misc_data[0][2]) == 0:
#            passport_misc_data = None

        form = EducationalQualificationsForm()
        educational_qualifications_collection_fieldnames = form.fields
        educational_qualifications_collection_fields = []
        for index, field in enumerate(educational_qualifications_collection_fieldnames):
            educational_qualifications_collection_fields.append([form.fields[field].label, field])
        #[['Class / Degree', 'class_degree'], ['Institute Name', 'institute_name'], ['University/Board/Council', 'university_board_council'], ['From', 'year_from'], ['To', 'year_to'], ['Marks Obtained', 'marks_obtained'], ['Total Marks', 'total_marks'], ['Percentage', 'percentage'], ['Proof', 'proof']]
        educational_qualifications_list = EducationalQualifications.objects.filter(candidate=candidate).values().order_by('id').exclude(class_degree__isnull=True).exclude(class_degree__exact="")
        educational_qualifications_collection = []
        for index, educational_qualifications in enumerate(educational_qualifications_list):
            educational_qualifications_collection.append([])
            for field in educational_qualifications_collection_fields:
                educational_qualifications_collection[index].append(educational_qualifications_list[index].get(field[1]))

        form = ProfessionalQualificationsForm()
        professional_qualifications_collection_fieldnames = form.fields
        professional_qualifications_collection_fields = []
        for index, field in enumerate(professional_qualifications_collection_fieldnames):
            professional_qualifications_collection_fields.append([form.fields[field].label, field])
#        professional_qualifications_collection_fields = [['Course', 'class_degree'], ['Institute Name', 'institute_name'], ['University/Council', 'university_board_council'], ['From', 'date_from'], ['To', 'date_to'], ['Marks Obtained', 'marks_obtained'], ['Total Marks', 'total_marks'], ['Percentage', 'percentage'], ['Proof', 'proof']]
        professional_qualifications_list = ProfessionalQualifications.objects.filter(candidate=candidate).values().order_by('id').exclude(institute_name__isnull=True).exclude(institute_name__exact="")
        professional_qualifications_collection = []
        for index, professional_qualifications in enumerate(professional_qualifications_list):
            professional_qualifications_collection.append([])
            for field in professional_qualifications_collection_fields:
                professional_qualifications_collection[index].append(professional_qualifications_list[index].get(field[1]))

        form = AdditionalQualificationsForm()
        additional_qualifications_collection_fieldnames = form.fields
        additional_qualifications_collection_fields = []
        for index, field in enumerate(additional_qualifications_collection_fieldnames):
            additional_qualifications_collection_fields.append([form.fields[field].label, field])
#        additional_qualifications_collection_fields = [['Class / Degree', 'class_degree'], ['Institute Name', 'institute_name'], ['University/Board/Council', 'university_board_council'], ['From', 'year_from'], ['To', 'year_to'], ['Marks Obtained', 'marks_obtained'], ['Total Marks', 'total_marks'], ['Percentage', 'percentage'], ['Proof', 'proof']]
        additional_qualifications_list = AdditionalQualifications.objects.filter(candidate=candidate).values().order_by('id').exclude(class_degree__isnull=True).exclude(class_degree__exact="")
        additional_qualifications_collection = []
        for index, additional_qualifications in enumerate(additional_qualifications_list):
            additional_qualifications_collection.append([])
            for field in additional_qualifications_collection_fields:
                additional_qualifications_collection[index].append(additional_qualifications_list[index].get(field[1]))

        form = StateNursingCouncilForm()
        state_nursing_council_collection_fieldnames = form.fields
        state_nursing_council_collection_fields = []
        for index, field in enumerate(state_nursing_council_collection_fieldnames):
            state_nursing_council_collection_fields.append([form.fields[field].label, field])
#        state_nursing_council_collection_fields = [['Class / Degree', 'class_degree'], ['Institute Name', 'institute_name'], ['University/Board/Council', 'university_board_council'], ['From', 'year_from'], ['To', 'year_to'], ['Marks Obtained', 'marks_obtained'], ['Total Marks', 'total_marks'], ['Percentage', 'percentage'], ['Proof', 'proof']]
        state_nursing_council_list = StateNursingCouncil.objects.select_related('state_nursing_council_name').exclude(state_nursing_council_name__name__isnull=True).exclude(state_nursing_council_name__name__exact="").filter(candidate=candidate).order_by('course', 'id').values()
#        pdb.set_trace()
        state_nursing_council_collection = []
        for index, state_nursing_council in enumerate(state_nursing_council_list):
            state_nursing_council_collection.append([])
            for field in state_nursing_council_collection_fields:
                if field[1].lower() == 'state_nursing_council_name':
                    state_nursing_council_name_id = state_nursing_council_list[index].get('state_nursing_council_name_id')
                    state_nursing_council_collection[index].append(StateNursingCouncilName.objects.get(pk=state_nursing_council_name_id).name)
                else:
                    state_nursing_council_collection[index].append(state_nursing_council_list[index].get(field[1]))

        form = EligibilityTestsForm()
        eligibility_tests_collection_fieldnames = form.fields
        eligibility_tests_collection_fields = []
        for index, field in enumerate(eligibility_tests_collection_fieldnames):
            eligibility_tests_collection_fields.append([form.fields[field].label, field])
#        eligibility_tests_collection_fields = [['Class / Degree', 'class_degree'], ['Institute Name', 'institute_name'], ['University/Board/Council', 'university_board_council'], ['From', 'year_from'], ['To', 'year_to'], ['Marks Obtained', 'marks_obtained'], ['Total Marks', 'total_marks'], ['Percentage', 'percentage'], ['Proof', 'proof']]
        eligibility_tests_list = EligibilityTests.objects.filter(candidate=candidate).values().order_by('id').exclude(score_grade_marks__isnull=True).exclude(score_grade_marks__exact="")
        eligibility_tests_collection = []
        for index, eligibility_tests in enumerate(eligibility_tests_list):
            eligibility_tests_collection.append([])
            for field in eligibility_tests_collection_fields:
                eligibility_tests_collection[index].append(eligibility_tests_list[index].get(field[1]))

        form = ExperienceForm()
        experience_collection_fieldnames = form.fields
        experience_collection_fields = []
        for index, field in enumerate(experience_collection_fieldnames):
            experience_collection_fields.append([form.fields[field].label, field])
#        experience_collection_fields = [['Class / Degree', 'class_degree'], ['Institute Name', 'institute_name'], ['University/Board/Council', 'university_board_council'], ['From', 'year_from'], ['To', 'year_to'], ['Marks Obtained', 'marks_obtained'], ['Total Marks', 'total_marks'], ['Percentage', 'percentage'], ['Proof', 'proof']]
        experience_list = Experience.objects.filter(candidate=candidate).values().order_by('id').exclude(institution__isnull=True).exclude(institution__exact="")
        experience_collection = []
        for index, experience in enumerate(experience_list):
            experience_collection.append([])
            for field in experience_collection_fields:
                experience_collection[index].append(experience_list[index].get(field[1]))

        registration_number_raw = candidate.registration_number
        registration_number = registration_number_raw.hashid
        is_provisional_registration_number = getattr(candidate, 'is_provisional_registration_number')
        displayed_registration_number = candidate.registration_number_display()

        if candidate.sent_email_notification_provisional_registration_number is False:
            current_site = get_current_site(request)
            user = candidate.candidate_username
            message = render_to_string('candidate/provisional_registration_number_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'registration_number_display': candidate.registration_number_display()
            })
            mail_subject = 'Your provisional TNAI recruitment registration number'
            to_email = candidate.candidate_username.username
            email = EmailMessage(mail_subject, message, to=[to_email])
            result = email.send()
            if result:
                candidate.sent_email_notification_provisional_registration_number = True
                candidate.save()

#        pdb.set_trace()
        return render(request, 'candidate/candidate_profile.html', {'candidate': candidate, 'personal_data': personal_data, 'address_data': address_data, 'passport_misc_data': passport_misc_data, 'educational_qualifications_collection_fields': educational_qualifications_collection_fields, 'educational_qualifications_collection': educational_qualifications_collection, 'professional_qualifications_collection_fields': professional_qualifications_collection_fields, 'professional_qualifications_collection': professional_qualifications_collection, 'additional_qualifications_collection_fields': additional_qualifications_collection_fields, 'additional_qualifications_collection': additional_qualifications_collection, 'state_nursing_council_collection_fields': state_nursing_council_collection_fields, 'state_nursing_council_collection': state_nursing_council_collection, 'eligibility_tests_collection_fields': eligibility_tests_collection_fields, 'eligibility_tests_collection': eligibility_tests_collection, 'experience_collection_fields': experience_collection_fields, 'experience_collection': experience_collection, 'registration_number': registration_number, 'displayed_registration_number': displayed_registration_number, 'updation_allowed': updation_allowed, 'ra_user': ra_user, })

    except ObjectDoesNotExist:
        fields = None
        return render(request, 'candidate/index.html', {'candidate': None})

def find_jobs(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    updation_allowed = False
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )

    queryset = []
    if request.method == 'POST':
        form = CandidateFindJobsForm(request.POST)
        if form.is_valid():
            queryset = Advertisement.objects.all()
            country = form.cleaned_data['country']
            if country is not None and len(country) > 0:
                queryset = Advertisement.objects.filter(country__icontains=country)
    else:
        form = CandidateFindJobsForm()

    return render(request, 'candidate/find_jobs.html', {'form': form, 'queryset': queryset, }, )

def booked_exam_time_slots(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    updation_allowed = False
    if not allowed:
        return render(request, 'candidate/not_allowed.html', {'next': request.path}, )
    candidate = Candidate.objects.get(candidate_username=username)
    exam_or_interview = request.GET.__getitem__('exam_or_interview')

    queryset = CandidateBookTimeSlot.objects.filter(candidate=candidate).select_related('exam').filter(exam__exam_or_interview = exam_or_interview)
    return render(request, 'candidate/booked_exam_time_slots.html', {'candidate': candidate, 'queryset': queryset, 'exam_or_interview': exam_or_interview})

class DetailView(generic.DetailView):
    model = Candidate
    template_name = 'candidate/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        username=get_acting_user(self.request)
        return Candidate.objects.filter(candidate_username=username)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = user.username
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('candidate/acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your candidate account.'
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponseRedirect('/candidate/first_activation/')
    
    else:
        form = SignupForm()
    
    return render(request, 'candidate/signup.html', {'form': form})

def first_activation(request):
    return render(request, 'candidate/first_activation.html', )

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
#        login(request, user)
        # return redirect('home')

        g = Group.objects.get(name='Candidate') 
        g.user_set.add(user)

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#class CandidateEducationalQualificationCreate(CreateView):
#    model = Candidate
