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

import pdb
    
class ExamForm(ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%y', '%d.%m.%Y'], required=False, label='Date (DD-MM-YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}), )
    hall_ticket_download_last_date = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%y', '%d.%m.%Y'], required=False, label='Hall ticket download last date (DD-MM-YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}), )
    class Meta:
        model = Exam
        fields = ['exam_type', 'advertisement', 'name', 'date', 'hall_ticket_download_last_date', ]

class ExamTimeSlotForm(ModelForm):
    begin_time = forms.TimeField(input_formats=['%H:%M'], required=False, label='Begin', widget=forms.TimeInput(format=('%H:%M'), attrs={'size':'15'}))
    end_time = forms.TimeField(input_formats=['%H:%M'], required=False, label='End', widget=forms.TimeInput(format=('%H:%M'), attrs={'size':'15'}))
    class Meta:
        model = ExamTimeSlot
        fields = '__all__'

class FilterExamListForm(forms.Form):
    EXAM_TYPE_CHOICES = [(None, '--- Any ---')]
    EXAM_TYPE_CHOICES.extend(Exam.exam_type_choices())
    exam_name = forms.CharField(max_length=500, required=False, label='Name')
    exam_date = forms.DateField(input_formats=['%d/%m/%y', '%d-%m-%y', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%y', '%d.%m.%Y'], required=False, label='Date (DD-MM-YY)', widget=forms.DateInput(format=('%d/%m/%y'), attrs={'size':'15'}), )
    exam_type = forms.ChoiceField(choices=EXAM_TYPE_CHOICES, required=False, label='Type')
#    only_show_interesting = forms.BooleanField(initial=False, required = False)

class CandidateBookTimeSlotForm(forms.Form):
    TIME_SLOT_CHOICES = []
    time_slot = forms.ChoiceField(choices=TIME_SLOT_CHOICES, widget=forms.RadioSelect())
    def __init__(self, *args, **kwargs):
        try:
            queryset = kwargs.pop('queryset')
        except KeyError:
            queryset = []
        try:
            booked_time_slot = kwargs.pop('booked_time_slot')
        except KeyError:
            booked_time_slot = None

        super(CandidateBookTimeSlotForm, self).__init__(*args, **kwargs)
        choices = []
        for record in queryset:
            time_slot_string = str(record.begin_time.strftime('%H:%M')) + ' to ' + str(record.end_time.strftime('%H:%M'))
            choices.append((record.pk, time_slot_string))

        self.fields['time_slot'].choices = choices
        if booked_time_slot is not None:
            self.fields['time_slot'].initial = booked_time_slot.pk

class ShowInterestInExamForm(forms.Form):
    interested = forms.BooleanField(initial = True, required = False)
