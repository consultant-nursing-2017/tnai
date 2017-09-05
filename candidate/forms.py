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

class StateNursingCouncilForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['degree_recognized_by_INC', 'state_nursing_council_name', 'state_nursing_council_registration_number', 'state_nursing_council_registration_date', 'state_nursing_council_proof']

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
                'grade': forms.TextInput(attrs={'size':'5'}),
                }

class ProfessionalQualificationsForm(ModelForm):
    class Meta:
        model = ProfessionalQualifications
        fields = ['class_degree', 'institute_name', 'university_board_council', 'date_from', 'date_to', 'marks_obtained', 'total_marks', 'percentage', 'grade', 'proof']
        labels = {'class_degree': 'Course', 'university_board_council': 'University/Council', 'percentage': 'Percent', 'grade': 'Grade/Division', 'date_from': 'From (MM/YY)', 'date_to': 'To (MM/YY)', }
        widgets = {
                'class_degree': forms.TextInput(attrs={'size':'10', 'placeholder':'Degree (specify)'}),
#                'institute_name': forms.Textarea(attrs={'rows':3, 'cols':25, 'placeholder': 'Institute Name'},),
                'marks_obtained': forms.TextInput(attrs={'size':'5'}),
                'total_marks': forms.TextInput(attrs={'size':'5'}),
                'percentage': forms.TextInput(attrs={'size':'5'}),
                'date_from': forms.TextInput(attrs={'size':'15', 'input_formats': '[\'%m/%Y\']', }),
                'date_to': forms.TextInput(attrs={'size':'15', 'input_formats' :'[\'%m/%Y\']', }),
                'grade': forms.TextInput(attrs={'size':'5'}),
                }

class AdditionalQualificationsForm(ModelForm):
    class Meta:
        model = AdditionalQualifications
        exclude = ['candidate']
        labels = {'completed_on': 'Completed On (MM/YY)'}
        widgets = {
                'course_name': forms.TextInput(attrs={'size':'25', 'placeholder':'Course (specify)'}),
                'completed_onn': forms.TextInput(attrs={'size':'15', 'input_formats': '[\'%m/%Y\']', }),
                }

class EligibilityTestsForm(ModelForm):
    class Meta:
        model = EligibilityTests
        exclude = ['candidate']
        labels = {'eligibility_tests': 'Test/Exam', 'score_grade_marks': 'Score/Grade/Marks', 'completed_on': 'Completed on (DD/MM/YY)', 'valid_up_to': 'Valid Up to (DD/MM/YY)',}
        widgets = {
                'eligibility_tests': forms.TextInput(attrs={'size':'25', 'placeholder':'Other (specify)'}),
                }

#    def __init__(self, *args, **kwargs):
#        super (EligibilityTestsForm,self ).__init__(*args, **kwargs) # populates the post
#        self.fields['user'] = self.instance.candidate_username

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ['candidate']
        labels = {'year_from': 'From (DD/MM/YY)', 'year_to': 'To (DD/MM/YY)'}

class StateNursingCouncilForm(ModelForm):
#    s_no = forms.CharField(max_length=5, disabled=True)
#    courses = forms.CharField(max_length=10, disabled=True)
    class Meta:
        model = StateNursingCouncil
        fields = ['course', 'state', 'registration_number', 'year', ]

class PassportAndMiscForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['passport_number', 'passport_valid_from', 'passport_valid_to', 'passport_place_of_issue', 'tnai_number', 'preference_of_work']

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}
