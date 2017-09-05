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
from .models import Candidate, EducationalQualifications, ProfessionalQualifications, AdditionalQualifications, EligibilityTests, Experience
from .forms import SubmitForm, PersonalForm, StateNursingCouncilForm, EducationalQualificationsForm, ProfessionalQualificationsForm, AdditionalQualificationsForm, EligibilityTestsForm, ExperienceForm, PassportAndMiscForm
from django.core.mail import send_mail
import hashlib
import random
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

##from django.contrib.auth.decorators import permission_required


#def index(request):
#    return HttpResponse("You're at the submit_contributions index.")

class IndexView(generic.ListView):
    template_name = 'candidate/index.html'
    context_object_name = 'candidate_list'

    def get_queryset(self):
        """Return the last five published questions."""
        username=auth.get_user(self.request)
        if username.is_authenticated():
            return Candidate.objects.filter(candidate_username=username)
        else:
            return HttpResponse("No profile available.")

def redirect_to_tab(request):
        if 'personal' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_personal/')
        elif 'educational' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_educational_qualifications/')
        elif 'professional' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_professional_qualifications/')
        elif 'additional' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_additional_qualifications/')
        elif 'experience' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_experience/')
        elif 'eligibility' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_eligibility_tests/')
        elif 'state_nursing_council' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_snc/')
        elif 'passport' in request.POST:
            return HttpResponseRedirect('/candidate/submit_candidate_passport/')
        else:
            return HttpResponseRedirect('/candidate/candidate_list/')
 

def submit_candidate(request):
    # if this is a POST request we need to process the form data
    username=auth.get_user(request)
#    EducationalQualificationsFormSet = inlineformset_factory(Candidate, EducationalQualifications, form=EducationalQualificationsForm, extra = 7)
    EligibilityTestsFormSet = inlineformset_factory(Candidate, EligibilityTests, form=EligibilityTestsForm, extra = 8)
#    ExperienceFormSet = inlineformset_factory(Candidate, Experience, form=ExperienceForm, extra = 5)
    new_profile = True
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
#        form = SubmitForm(request.POST, request.FILES)
        # check whether it's valid:
        # TODO

        try:
            candidate = Candidate.objects.get(candidate_username=username)
            submit_form = SubmitForm(request.POST, request.FILES, instance=candidate)
            if submit_form.is_valid():
                submit_form.save()
#            candidate = Candidate.objects.get(candidate_username=username)
            new_profile = False
        except ObjectDoesNotExist:
            submit_form = SubmitForm(request.POST, request.FILES)
            if submit_form.is_valid():
                submit_form.save()
            candidate = Candidate.objects.get(candidate_username=username)
            new_profile = True

#        state_nursing_council_form = StateNursingCouncilForm(request.POST, request.FILES, instance=candidate)
#
#        if state_nursing_council_form.is_valid():
##            degree_recognized_by_INC = state_nursing_council_form.cleaned_data['degree_recognized_by_INC']
##            state_nursing_council_name = state_nursing_council_form.cleaned_data['state_nursing_council_name']
##            state_nursing_council_registration_number = state_nursing_council_form.cleaned_data['state_nursing_council_registration_number']
##            state_nursing_council_registration_date = state_nursing_council_form.cleaned_data['state_nursing_council_registration_date']
##            state_nursing_council_proof = state_nursing_council_form.cleaned_data['state_nursing_council_proof']
#            state_nursing_council_form.save()
#            candidate = Candidate.objects.get(candidate_username=username)

#        educational_qualifications_formset = EducationalQualificationsFormSet(request.POST, request.FILES, instance=candidate)
#        educational_qualifications_form_instance = EducationalQualificationsForm()
#        if educational_qualifications_formset.is_valid():
#            educational_qualifications_formset.save()
#            candidate = Candidate.objects.get(candidate_username=username)
        eligibility_tests_formset = EligibilityTestsFormSet(request.POST, request.FILES, instance=candidate)#, initial={'user': username,})
        eligibility_tests_form_instance = EligibilityTestsForm()
        if eligibility_tests_formset.is_valid():
            eligibility_tests_formset.save()
#            candidate = Candidate.objects.get(candidate_username=username)
#        experience_formset = ExperienceFormSet(request.POST, request.FILES, instance=candidate)
#        experience_form_instance = ExperienceForm()
#        if experience_formset.is_valid():
#            experience_formset.save()
#            candidate = Candidate.objects.get(candidate_username=username)

#            passport_number = passport_and_misc_form.cleaned_data['passport_number']
#            passport_valid_from = passport_and_misc_form.cleaned_data['passport_valid_from']
#            passport_valid_to = passport_and_misc_form.cleaned_data['passport_valid_to']
#            passport_place_of_issue = passport_and_misc_form.cleaned_data['passport_place_of_issue']
#            preference_of_work = passport_and_misc_form.cleaned_data['preference_of_work']
#        passport_and_misc_form = PassportAndMiscForm(request.POST, request.FILES, instance=candidate)
#            if passport_and_misc_form.is_valid():
#                passport_and_misc_form.save()
  
# TODO            photograph
            return HttpResponseRedirect('/candidate/candidate_list/')

            # if a GET (or any other method) we'll create a blank form
    else:
        try:
            candidate = Candidate.objects.get(candidate_username=username)
            submit_form = SubmitForm(instance=candidate)
#            educational_qualifications_formset = EducationalQualificationsFormSet(instance=candidate)
#            educational_qualifications_form_instance = EducationalQualificationsForm()
            eligibility_tests_formset = EligibilityTestsFormSet(instance=candidate)#, initial={'user': username,})
            eligibility_tests_form_instance = EligibilityTestsForm()
#            experience_formset = ExperienceFormSet(request.POST, request.FILES, instance=candidate)
#            experience_form_instance = ExperienceForm()
            new_profile = False
        except ObjectDoesNotExist:
            submit_form = SubmitForm(initial={'candidate_username': username,})
#            educational_qualifications_formset = EducationalQualificationsFormSet()
#            educational_qualifications_form_instance = EducationalQualificationsForm()
            eligibility_tests_formset = EligibilityTestsFormSet()#initial={'user': username,})
            eligibility_tests_form_instance = EligibilityTestsForm()
#            experience_formset = ExperienceFormSet()
#            experience_form_instance = ExperienceForm()
            new_profile = True

    return render(request, 'candidate/submit_candidate.html', {'new_profile': new_profile, 'submit_form': submit_form, 'eligibility_tests_formset': eligibility_tests_formset, 'eligibility_tests_form_instance': eligibility_tests_form_instance, })#educational_qualifications_formset': educational_qualifications_formset, 'educational_qualifications_form_instance': educational_qualifications_form_instance,})# 'experience_formset': experience_formset, 'experience_form_instance': experience_form_instance})

def submit_candidate_personal(request):
    username=auth.get_user(request)
    new_profile = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            candidate = Candidate.objects.get(candidate_username=username)
            personal_form = PersonalForm(request.POST, request.FILES, instance=candidate)
            if personal_form.is_valid():
                personal_form.save()
#            candidate = Candidate.objects.get(candidate_username=username)
            new_profile = False
        except ObjectDoesNotExist:
            personal_form = PersonalForm(request.POST, request.FILES)
            if personal_form.is_valid():
                personal_form.save()
            candidate = Candidate.objects.get(candidate_username=username)
            new_profile = True

        return redirect_to_tab(request)
            # if a GET (or any other method) we'll create a blank form
    else:
        try:
            candidate = Candidate.objects.get(candidate_username=username)
            personal_form = PersonalForm(instance=candidate)
            new_profile = False
        except ObjectDoesNotExist:
            personal_form = PersonalForm(initial={'candidate_username': username,})
            new_profile = True

    return render(request, 'candidate/submit_candidate_personal.html', {'new_profile': new_profile, 'personal_form': personal_form,}) 

def submit_candidate_educational_qualifications(request):
    username=auth.get_user(request)
    new_profile = False
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        not_professional_qualifications_queryset = EducationalQualifications.objects.filter(candidate=candidate, professionalqualifications__isnull=True)
#        not_professional_qualifictions_queryset = [p for p in educational_queryset if not hasattr(p, 'professionalqualifications')]
        num_educational_qualifications = not_professional_qualifications_queryset.count()
        if num_educational_qualifications > 3:
            raise ValidationError(_('num_educational_qualifications is greater than 3, value: %(value)s'), params={'value': 'num_educational_qualifications'},)
        extra_forms = 3 - num_educational_qualifications
        EducationalQualificationsFormSet = inlineformset_factory(Candidate, EducationalQualifications, form=EducationalQualificationsForm, extra=extra_forms, can_delete=False)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')
    if request.method == 'POST':
        # check whether it's valid:
        # TODO
        educational_qualifications_formset = EducationalQualificationsFormSet(request.POST, request.FILES, instance=candidate, queryset=not_professional_qualifications_queryset)#, initial={'user': username,})
        educational_qualifications_form_instance = EducationalQualificationsForm()
        if educational_qualifications_formset.is_valid():
            educational_qualifications_formset.save()

        return redirect_to_tab(request)

    else:
        if num_educational_qualifications > 0:
            educational_qualifications_formset = EducationalQualificationsFormSet(instance=candidate, queryset=not_professional_qualifications_queryset)#, initial={'user': username,})
        else:
            educational_qualifications_formset = EducationalQualificationsFormSet(instance=candidate,
                initial=[{'class_degree': '10th'}, {'class_degree': '12th/Equivalent'}], queryset=not_professional_qualifications_queryset) #, initial={'user': username,})
        educational_qualifications_form_instance = EducationalQualificationsForm()

    return render(request, 'candidate/submit_candidate_educational_qualifications.html', {'educational_qualifications_formset': educational_qualifications_formset, 'educational_qualifications_form_instance': educational_qualifications_form_instance, })

def submit_candidate_professional_qualifications(request):
    username=auth.get_user(request)
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
        professional_qualifications_form_instance = ProfessionalQualificationsForm()
        if professional_qualifications_formset.is_valid():
            professional_qualifications_formset.save()

        return redirect_to_tab(request)
    else:
        if num_professional_qualifications > 0:
            professional_qualifications_formset = ProfessionalQualificationsFormSet(instance=candidate)#, initial={'user': username,})
        else:
            professional_qualifications_formset = ProfessionalQualificationsFormSet(instance=candidate,
                initial=[{'class_degree': 'ANM'}, {'class_degree': 'GNM'}, {'class_degree': 'B. Sc.(N)'}, {'class_degree': 'P. B. B. Sc.(N)'}, {'class_degree': 'M. Sc.(N)'},]) #, initial={'user': username,})
        professional_qualifications_form_instance = ProfessionalQualificationsForm()

    return render(request, 'candidate/submit_candidate_professional_qualifications.html', {'professional_qualifications_formset': professional_qualifications_formset, 'professional_qualifications_form_instance': professional_qualifications_form_instance, })

def submit_candidate_additional_qualifications(request):
    username=auth.get_user(request)
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
        additional_qualifications_form_instance = AdditionalQualificationsForm()
        if additional_qualifications_formset.is_valid():
            additional_qualifications_formset.save()

        return redirect_to_tab(request)
    else:
        if num_additional_qualifications > 0:
            additional_qualifications_formset = AdditionalQualificationsFormSet(instance=candidate)#, initial={'user': username,})
        else:
            additional_qualifications_formset = AdditionalQualificationsFormSet(instance=candidate,
                initial=[{'course_name': 'M. Phil'}, {'course_name': 'PhD'}, {'course_name': 'MBA'}, {'course_name': 'Post Certificate'}, {'course_name': 'Post Degree'},]) #, initial={'user': username,})
        additional_qualifications_form_instance = AdditionalQualificationsForm()

    return render(request, 'candidate/submit_candidate_additional_qualifications.html', {'additional_qualifications_formset': additional_qualifications_formset, 'additional_qualifications_form_instance': additional_qualifications_form_instance, })

def submit_candidate_experience(request):
    username=auth.get_user(request)
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
        experience_form_instance = ExperienceForm()
        if experience_formset.is_valid():
            experience_formset.save()

        return redirect_to_tab(request)
    else:
        experience_formset = ExperienceFormSet(instance=candidate,) #, initial={'user': username,})
        experience_form_instance = ExperienceForm()

    return render(request, 'candidate/submit_candidate_experience.html', {'experience_formset': experience_formset, 'experience_form_instance': experience_form_instance, })

def submit_candidate_eligibility_tests(request):
    username=auth.get_user(request)
    try:
        candidate = Candidate.objects.get(candidate_username=username)
        num_eligibility_tests = EligibilityTests.objects.filter(candidate=candidate).count()
        if num_eligibility_tests > 8:
            raise ValidationError(_('num_eligibility_tests is greater than 8, value: %(value)s'), params={'value': 'num_eligibility_tests'},)
        extra_forms = 8 - num_eligibility_tests
        EligibilityTestsFormSet = inlineformset_factory(Candidate, EligibilityTests, form=EligibilityTestsForm, extra=extra_forms, can_delete=False)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/candidate/submit_candidate_personal/')

    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        eligibility_tests_formset = EligibilityTestsFormSet(request.POST, request.FILES, instance=candidate)#, initial={'user': username,})
        eligibility_tests_form_instance = EligibilityTestsForm()
        if eligibility_tests_formset.is_valid():
            eligibility_tests_formset.save()

        return redirect_to_tab(request)
    else:
        if num_eligibility_tests > 0:
            eligibility_tests_formset = EligibilityTestsFormSet(instance=candidate)#, initial={'user': username,})
        else:
            eligibility_tests_formset = EligibilityTestsFormSet(instance=candidate,
                initial=[{'eligibility_tests': 'Prometric (Specify country)'}, {'eligibility_tests': 'HAAD'}, {'eligibility_tests': 'GHA'}, {'eligibility_tests': 'IELTS'}, {'eligibility_tests': 'CGFNS'}, {'eligibility_tests': 'TOEFL'}, {'eligibility_tests': 'OET'},]) #, initial={'user': username,})

        eligibility_tests_form_instance = EligibilityTestsForm()

    return render(request, 'candidate/submit_candidate_eligibility_tests.html', {'eligibility_tests_formset': eligibility_tests_formset, 'eligibility_tests_form_instance': eligibility_tests_form_instance, })

def submit_candidate_passport(request):
    username=auth.get_user(request)
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
    pass

class DetailView(generic.DetailView):
    model = Candidate
    template_name = 'candidate/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Candidate.objects.all()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('candidate_acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your candidate account.'
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    
    else:
        form = SignupForm()
    
    return render(request, 'candidate_signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')

        g = Group.objects.get(name='Candidate') 
        g.user_set.add(user)

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#class CandidateEducationalQualificationCreate(CreateView):
#    model = Candidate
