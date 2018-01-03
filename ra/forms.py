from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from candidate.models import ProfessionalQualifications, EligibilityTests, Candidate
from .models import RA
from .models import CandidateList

import pdb
    
class FilterForm(forms.Form):
    name = forms.CharField(required=False, )
    date_of_birth = forms.DateField(required=False, )
    gender = forms.ChoiceField([(None, '--- Either ---'), ('Male', 'Male'), ('Female', 'Female'), ], required=False, )
    COURSE_CHOICES = [(None, '--- Any ---')]
    COURSES = ProfessionalQualifications.course_choices()
    for course in COURSES:
        COURSE_CHOICES.append((course, course))
    professional_qualifications = forms.ChoiceField(COURSE_CHOICES, required=False, )
    minimum_experience = forms.CharField(required=False, )
    ELIGIBILITY_TESTS_CHOICES = [(None, '--- Any ---')] + list(EligibilityTests.eligibility_tests_choices())
    eligibility_tests = forms.ChoiceField(ELIGIBILITY_TESTS_CHOICES, required=False,)

class CandidateListForm(ModelForm):
    non_members = forms.ModelMultipleChoiceField(required = False, queryset = None, label = "Non-members")
    class Meta:
        model = CandidateList
        fields = ['name', 'members', 'non_members', 'notes', 'exam', 'exam_list_type', 'employer', 'advertisement']

    def __init__(self, *args, **kwargs):
        super (ModelForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        qs = instance.members.order_by('name')
        complement_qs = Candidate.objects.exclude(pk__in = qs).order_by('name')
        self.fields['members'].queryset = qs
        self.fields['members'].required = False
        self.fields['non_members'].queryset = complement_qs

class ActAsForm(ModelForm):
    class Meta:
        model = RA
        fields = ['logged_in_as', 'acting_as']
        widgets = {'logged_in_as': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super (ActAsForm,self ).__init__(*args, **kwargs) # populates the post
        qs = Group.objects.get(name='Employer').user_set.all() | Group.objects.get(name='Candidate').user_set.all()
        self.fields['acting_as'].queryset = qs

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}
