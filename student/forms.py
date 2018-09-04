from django import forms
from django.forms import ModelForm
from .models import Student, TakeExam
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

from instructor.models import Answer, Exam
import pdb
    
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class TakeExamForm(ModelForm):
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super (TakeExamForm,self ).__init__(*args, **kwargs) # populates the post
        private_exam_queryset = Exam.objects.filter(students__in=[student])
        public_exam_queryset = Exam.objects.filter(is_public = True)
        self.fields['exam'].queryset = (private_exam_queryset | public_exam_queryset).distinct()

    class Meta:
        model = TakeExam
        fields = ['exam']

class ShowQuestionInExamForm(ModelForm):
    answer = forms.ModelChoiceField(queryset = Answer.objects.all(), required = False)

    def __init__(self, *args, **kwargs):
        super (ShowQuestionInExamForm,self ).__init__(*args, **kwargs) # populates the post
        instance = kwargs.pop('instance')
        question_number = instance.current_question
        if question_number >= instance.exam.questions.count():
            raise ValidationError(_("Question number exceeds total number of questions in exam."), code='question_number_out_of_bounds')

        question = instance.exam.questions.all()[question_number]
        self.fields['answer'].queryset = Answer.objects.filter(question = question).order_by('text')

    class Meta:
        model = TakeExam
        fields = ['answer']
