from django import forms
from django.forms import ModelForm
from .models import Instructor, Topic, Question, Answer
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

class SignupForm(UserCreationForm):
#    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Email address (will also serve as your username)'}

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower()
