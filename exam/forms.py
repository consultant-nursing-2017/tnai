from django import forms
from django.forms import ModelForm
from .models import Exam, ExamTimeSlots, CandidateBookTimeSlot
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

class ExamTimeSlotsForm(ModelForm)
    class Meta:
        model = ExamTimeSlots
        fields = '__all__'

class CandidateBookTimeSlotForm(ModelForm)
    class Meta:
        model = CandidateBookTimeSlot
        fields = '__all__' 
