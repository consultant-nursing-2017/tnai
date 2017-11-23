from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.template import Context
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
class ContactForm(forms.Form):
    name = forms.CharField(required=True, )
    email = forms.EmailField(required=True, )
    phone_number = forms.CharField(required=True, max_length=15)
    message = forms.CharField(required=True, )
