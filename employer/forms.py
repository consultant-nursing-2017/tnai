from django import forms
from django.forms import ModelForm
from .models import Employer, Advertisement
#from django.contrib.auth.models import User, Group
#from django.contrib.admin import widgets 

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tnai.widgets import CustomClearableFileInput
    
class EmployerForm(ModelForm):
#    def __init__(self, *args, **kwargs):
#        super (EmployerForm,self ).__init__(*args, **kwargs) # populates the post
#        self.fields['registration_certification'].required = False
#        self.fields['authorized_signatory_id_proof'].required = False
#        self.fields['total_employees'].required = False
#        self.fields['authorized_signatory_ID_proof'].required = False
#        self.fields['authorized_signatory_ID_proof'].required = False
#        sponsorsQS = Group.objects.filter(name='Sponsors')
#        self.fields['sponsor'].queryset = User.objects.filter(groups__in=sponsorsQS)
#        contributorsQS = Group.objects.filter(name='Contributors')
#        self.fields['contributor'].queryset = User.objects.filter(groups__in=contributorsQS)

    @staticmethod
    def fields_part1():
        return ['employer_username', 'name', 'country', 'registration', 'type', 'authorized_signatory', 'sector', 'address', 'website', 'phone']

    @staticmethod
    def fields_part2():
        return ['registration_certification', 'authorized_signatory_id_proof', 'total_employees', 'annual_recruitment_of_indians', 'nurses_degree', 'nurses_diploma', 'doctors', 'lab_technicians', 'pathologists']

    class Meta:
        model = Employer
        fields = '__all__' #['contributor', 'sponsor', 'url', 'date_submitted', 'approved']
        widgets = {'authorized_signatory_id_proof': CustomClearableFileInput, 'registration_certification': CustomClearableFileInput, }
#        widgets={'date_submitted': forms.DateTimeInput(format='%Y-%m-%d %H:%M')}

 
class AdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'
#        widgets={'': forms.DateTimeInput(format='%Y-%m-%d %H:%M')}

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower()
