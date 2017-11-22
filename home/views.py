from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import pdb
import os
import hashlib
import random

##from django.contrib.auth.decorators import permission_required


def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def recruitment(request):
    return render(request, 'home/recruitment.html')

def contact(request):
    return render(request, 'home/contact.html')

def media(request):
    return render(request, 'home/media.html')
