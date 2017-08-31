from django import forms
from django.forms import ModelForm
from .models import Candidate, EducationalQualifications, EligibilityTests
#from django.contrib.auth.models import User, Group
#from django.contrib.admin import widgets 

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
class PersonalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super (PersonalForm,self ).__init__(*args, **kwargs) # populates the post
#        self.fields['candidate_username'].disabled=True
#        self.fields['registration_certification'].required = False
#        self.fields['authorized_signatory_id_proof'].required = False
#        self.fields['total_employees'].required = False
#        self.fields['authorized_signatory_ID_proof'].required = False
#        self.fields['authorized_signatory_ID_proof'].required = False
#        sponsorsQS = Group.objects.filter(name='Sponsors')
#        self.fields['sponsor'].queryset = User.objects.filter(groups__in=sponsorsQS)
#        contributorsQS = Group.objects.filter(name='Contributors')
#        self.fields['contributor'].queryset = User.objects.filter(groups__in=contributorsQS)

    class Meta:
        model = Candidate
        fields = ['candidate_username', 'name', 'fathers_name', 'date_of_birth', 'gender', 'tnai_number', 'marital_status', 'email', 'address_line_1', 'address_line_2', 'district']

class StateNursingCouncilForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['degree_recognized_by_INC', 'state_nursing_council_name', 'state_nursing_council_registration_number', 'state_nursing_council_registration_date', 'state_nursing_council_proof']

class EducationalQualificationsForm(ModelForm):
    class Meta:
        model = EducationalQualifications
        fields = '__all__'

class EligibilityTestsForm(ModelForm):
    class Meta:
        model = EligibilityTests
        fields = '__all__'

class PassportAndMiscForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['passport_number', 'passport_valid_from', 'passport_valid_to', 'passport_place_of_issue', 'preference_of_work']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
