from django import forms
from django.forms import ModelForm
from .models import Instructor, Topic, Question, Answer, QuestionBank, Exam
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

import pdb
    
class InstructorForm(ModelForm):
    class Meta:
        model = Instructor
        fields = '__all__'

class TopicForm(ModelForm):
    all_topics = forms.ModelChoiceField(queryset = Topic.objects.all(), required = False)
    class Meta:
        model = Topic
        fields = '__all__'

class QuestionForm(ModelForm):
#    all_questions = forms.ModelChoiceField(queryset = Question.objects.all(), required = False)
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {'text': forms.Textarea(attrs = {'cols': 80, 'rows': 5}), }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ['question']

class QuestionBankForm(ModelForm):
    class Meta:
        model = QuestionBank
        fields = '__all__'
        widgets = {'questions': forms.CheckboxSelectMultiple(), }

class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {'students': forms.CheckboxSelectMultiple(), 'questions': forms.CheckboxSelectMultiple(), }

class FilterByTopicForm(forms.Form):
    topic = forms.ModelChoiceField(queryset = Topic.objects.all(), required = False) #, empty_label = "")
    def __init__(self, *args, **kwargs):
        exam = None
        try:
            exam = kwargs.pop('exam')
        except KeyError:
            pass
        super (FilterByTopicForm,self ).__init__(*args, **kwargs) # populates the post
        if exam is not None:
            exam_topics = exam.questions.all().values('topic').distinct()
            self.fields['topic'].queryset = self.fields['topic'].queryset.filter(topic_for_question__in=exam_topics)

class FilterExamByTopicForm(forms.Form):
    topic = forms.ModelChoiceField(queryset = Topic.objects.all(), required = True) #, empty_label = "")
    exam = forms.ModelChoiceField(queryset = Exam.objects.all(), required = True)

class ExamQuestionsForm(forms.Form):
    questions = forms.ModelMultipleChoiceField(queryset = Question.objects.all(), widget = forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        arg_topic = kwargs.pop('arg_topic')
        arg_exam = kwargs.pop('arg_exam')
        already_chosen_questions = arg_exam.questions.all()
        super (ExamQuestionsForm,self ).__init__(*args, **kwargs) # populates the post
        self.fields['questions'].queryset = self.fields['questions'].queryset.filter(topic = arg_topic).difference(already_chosen_questions)

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower()
