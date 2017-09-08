from django import forms
from django.forms import ModelForm
from .models import Candidate, EducationalQualifications, ProfessionalQualifications, AdditionalQualifications, EligibilityTests, Experience, StateNursingCouncil
#from django.contrib.auth.models import User, Group
#from django.contrib.admin import widgets 

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import pdb
    
class SubmitForm(ModelForm):
#    def __init__(self, *args, **kwargs):
#        super (SubmitForm,self ).__init__(*args, **kwargs) # populates the post
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
        exclude = []

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
        fields = ['candidate_username', 'name', 'fathers_name', 'date_of_birth', 'gender', 'marital_status', 'phone_number', 
            'house_number', 'area_locality', 'street_name', 'village_PS_PO', 'country', 'state', 'district', 'pin_code']

class EducationalQualificationsForm(ModelForm):
    class Meta:
        model = EducationalQualifications
        exclude = ['candidate']
        labels = {'university_board_council': 'University/Board', 'class_degree': 'Class/Degree', 'percentage': 'Percent'}
        widgets = {
                'class_degree': forms.TextInput(attrs={'size':'25', 'placeholder':'Degree (specify)'}),
#                'institute_name': forms.Textarea(attrs={'rows':3, 'cols':25, 'placeholder': 'Institute Name'},),
                'marks_obtained': forms.TextInput(attrs={'size':'5'}),
                'total_marks': forms.TextInput(attrs={'size':'5'}),
                'percentage': forms.TextInput(attrs={'size':'5'}),
#                'grade': forms.TextInput(attrs={'size':'5'}),
                }

    def clean(self):
        cleaned_data = super (ModelForm, self).clean()
        year_from = cleaned_data.get("year_from")
        year_to = cleaned_data.get("year_to")
        marks_obtained = cleaned_data.get("marks_obtained")
        total_marks = cleaned_data.get("total_marks")
#        pdb.set_trace()
        errors = []
        if year_from is not None and (year_to is None or year_from > year_to):
            errors.append(forms.ValidationError(_("'Year from' must be at most 'Year to'"), code='invalid_year'))
        if marks_obtained is not None and (total_marks is None or marks_obtained > total_marks):
            errors.append(forms.ValidationError(_("'Marks obtained' must be at most 'Total marks'"), code='invalid_marks'))
        if errors:
            raise ValidationError(errors)

class ProfessionalQualificationsForm(ModelForm):
    date_from = forms.DateField(input_formats=['%m/%y', '%m-%y'], required=False, label='From (MM/YY)', widget=forms.DateInput(format=('%m/%y'), attrs={'size':'15'}))
    date_to = forms.DateField(input_formats=['%m/%y', '%m-%y'], required=False, label='From (MM/YY)', widget=forms.DateInput(format=('%m/%y'), attrs={'size':'15'}))
    class Meta:
        model = ProfessionalQualifications
        fields = ['class_degree', 'institute_name', 'university_board_council', 'date_from', 'date_to', 'marks_obtained', 'total_marks', 'percentage', 'proof']
        labels = {'class_degree': 'Course', 'university_board_council': 'University/Council', 'percentage': 'Percent', 'date_from': 'From (MM/YY)', 'date_to': 'To (MM/YY)', }
        widgets = {
                'class_degree': forms.TextInput(attrs={'size':'10', 'placeholder':'Degree (specify)'}),
#                'institute_name': forms.Textarea(attrs={'rows':3, 'cols':25, 'placeholder': 'Institute Name'},),
                'marks_obtained': forms.TextInput(attrs={'size':'5'}),
                'total_marks': forms.TextInput(attrs={'size':'5'}),
                'percentage': forms.TextInput(attrs={'size':'5'}),
#                'date_from': forms.DateInput(format=('%m/%y'), attrs={'size':'15'}),
#                'date_to': forms.DateInput(format=('%m/%y'), attrs={'size':'15'}),
#                'grade': forms.TextInput(attrs={'size':'5'}),
                }

class AdditionalQualificationsForm(ModelForm):
    date_from = forms.DateField(input_formats=['%m/%y', '%m-%y'], required=False, label='From (MM/YY)', widget=forms.DateInput(format=('%m/%y'), attrs={'size':'15'}))
    date_to = forms.DateField(input_formats=['%m/%y', '%m-%y'], required=False, label='From (MM/YY)', widget=forms.DateInput(format=('%m/%y'), attrs={'size':'15'}))
    class Meta:
        model = AdditionalQualifications
        fields = ['class_degree', 'course_topic', 'institute_name', 'university_board_council', 'date_from', 'date_to', 'marks_obtained', 'total_marks', 'percentage', 'proof']
        labels = {'class_degree': 'Course', 'university_board_council': 'University/Council', 'percentage': 'Percent', 'date_from': 'From (MM/YY)', 'date_to': 'To (MM/YY)', }
        widgets = {
                'class_degree': forms.TextInput(attrs={'size':'10', 'placeholder':'Degree (specify)'}),
#                'institute_name': forms.Textarea(attrs={'rows':3, 'cols':25, 'placeholder': 'Institute Name'},),
                'marks_obtained': forms.TextInput(attrs={'size':'5'}),
                'total_marks': forms.TextInput(attrs={'size':'5'}),
                'percentage': forms.TextInput(attrs={'size':'5'}),
#                'date_from': forms.DateInput(attrs={'size':'15'}),
#                'date_to': forms.DateInput(attrs={'size':'15'}),
#                'grade': forms.TextInput(attrs={'size':'5'}),
                }

class EligibilityTestsForm(ModelForm):
    completed_on = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y'], required=False, label='Completed on (DD/MM/YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}))
    valid_up_to = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y'], required=False, label='Valid up to (DD/MM/YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}))
    class Meta:
        model = EligibilityTests
        exclude = ['candidate']
        labels = {'eligibility_tests': 'Test/Exam', 'completed_on': 'Completed on (DD/MM/YY)', 'valid_up_to': 'Valid up to (DD/MM/YY)',}
        widgets = {
                'eligibility_tests': forms.TextInput(attrs={'size':'25', 'placeholder':'Other (specify)'}),
                }

#    def __init__(self, *args, **kwargs):
#        super (EligibilityTestsForm,self ).__init__(*args, **kwargs) # populates the post
#        self.fields['user'] = self.instance.candidate_username

class ExperienceForm(ModelForm):
    date_from = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y'], required=False, label='From (DD/MM/YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}))
    date_to = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y'], required=False, label='From (DD/MM/YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}))
    class Meta:
        model = Experience
        exclude = ['candidate']
        labels = {'date_from': 'From (DD/MM/YY)', 'date_to': 'To (DD/MM/YY)'}

class StateNursingCouncilForm(ModelForm):
#    s_no = forms.CharField(max_length=5, disabled=True)
#    courses = forms.CharField(max_length=10, disabled=True)
    class Meta:
        model = StateNursingCouncil
        fields = ['course', 'state', 'registration_number', 'year', ]

class PassportAndMiscForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['passport_number', 'passport_valid_from', 'passport_valid_to', 'passport_place_of_issue', 'TNAI_number', 'preference_of_work']

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}
