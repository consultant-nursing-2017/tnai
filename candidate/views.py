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
from .models import Candidate, EducationalQualifications, EligibilityTests, Experience
from .forms import SubmitForm, PersonalForm, StateNursingCouncilForm, EducationalQualificationsForm, EligibilityTestsForm, ExperienceForm, PassportAndMiscForm
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
            to_email = form.cleaned_data.get('email')
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
