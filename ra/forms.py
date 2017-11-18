from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from candidate.models import ProfessionalQualifications, EligibilityTests
    
class FilterForm(forms.Form):
    name = forms.CharField(required=False, )
    date_of_birth = forms.DateField(required=False, )
    gender = forms.ChoiceField([(None, '--- Either ---'), ('Male', 'Male'), ('Female', 'Female'), ], required=False, )
    COURSE_CHOICES = [(None, '--- Any ---')]
    COURSES = ProfessionalQualifications.course_choices()
    for course in COURSES:
        COURSE_CHOICES.append((course, course))
    professional_qualifications = forms.ChoiceField(COURSE_CHOICES, required=False, )
    experience = forms.CharField(required=False, )
    ELIGIBILITY_TESTS_CHOICES = [(None, '--- Any ---')] + list(EligibilityTests.eligibility_tests_choices())
    eligibility_tests = forms.ChoiceField(ELIGIBILITY_TESTS_CHOICES, required=False,)

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}
