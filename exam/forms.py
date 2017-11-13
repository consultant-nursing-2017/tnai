from django import forms
from django.forms import ModelForm
from .models import Exam, ExamTimeSlot, CandidateBookTimeSlot
#from django.contrib.auth.models import User, Group
#from django.contrib.admin import widgets 

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
    
class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamTimeSlotForm(ModelForm):
    begin_time = forms.TimeField(input_formats=['%H:%M'], required=False, label='Begin', widget=forms.TimeInput(format=('%H:%M'), attrs={'size':'15'}))
    end_time = forms.TimeField(input_formats=['%H:%M'], required=False, label='End', widget=forms.TimeInput(format=('%H:%M'), attrs={'size':'15'}))
    class Meta:
        model = ExamTimeSlot
        fields = '__all__'

class CandidateBookTimeSlotForm(ModelForm):
    class Meta:
        model = CandidateBookTimeSlot
        fields = '__all__' 
