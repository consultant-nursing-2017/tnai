from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import Employer, Advertisement
from .forms import EmployerForm, AdvertisementForm
#from .forms import RegistrationForm
from django.core.mail import send_mail
import hashlib
import random
from django.utils.crypto import get_random_string
from django.contrib import auth

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

##from django.contrib.auth.decorators import permission_required


#def index(request):
#    return HttpResponse("You're at the submit_contributions index.")

class IndexView(generic.ListView):
    template_name = 'employer/index.html'
    context_object_name = 'employer_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Employer.objects.all()

def is_allowed(username, request):
    allowed = True
    if username.groups.filter(name="TNAI").count() <= 0:
        allowed = False
    
    return allowed

def employer_index(request):
    username=auth.get_user(request)
    object_does_not_exist = False
    if username.groups.filter(name="Candidate").count() > 0:
        return HttpResponseRedirect('/candidate/')

    try:
        if username.is_authenticated():
            employer = Employer.objects.get(employer_username=username)
        else:
            employer = None
    except ObjectDoesNotExist:
        employer = None
        object_does_not_exist = True

    return render(request, 'employer/index.html', {'employer': employer, 'object_does_not_exist': object_does_not_exist, }) 

def submit_employer(request):
    username=auth.get_user(request)
    new_profile = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            employer = Employer.objects.get(employer_username=username)
            new_profile = False
            form = EmployerForm(request.POST, request.FILES, instance=employer)
        except ObjectDoesNotExist:
            new_profile = True
            form = EmployerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/employer/')
    else:
        # if a GET (or any other method) we'll create a blank form
        try:
            employer = Employer.objects.get(employer_username=username)
            form = EmployerForm(instance=employer)
            new_profile = False
        except ObjectDoesNotExist:
            new_profile = True
            form = EmployerForm(initial={'employer_username': username,})

    return render(request, 'employer/submit_employer.html', {'new_profile': new_profile, 'form': form,}) 

def submit_advertisement(request):
    username=auth.get_user(request)
    new_advertisement = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            employer = Employer.objects.get(employer_username=username)
            advertisement = Advertisement.objects.get(employer_advert=employer)
            new_advertisement = False
            form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        except ObjectDoesNotExist:
            # TODO what if employer object doesn't exist
            new_advertisement = True
            form = AdvertisementForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/employer/')
    else:
        # if a GET (or any other method) we'll create a blank form
        try:
            employer = Employer.objects.get(employer_username=username)
            advertisement = Advertisement.objects.get(employer_advert=employer)
            form = AdvertisementForm(instance=advertisement)
            new_advertisement = False
        except ObjectDoesNotExist:
            new_advertisement = True
            form = AdvertisementForm(initial={'employer_advert': employer,})

    return render(request, 'employer/submit_advertisement.html', {'new_advertisement': new_advertisement, 'form': form,}) 

class DetailView(generic.DetailView):
    model = Employer
    template_name = 'employer/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Employer.objects.all()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('employer/acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your employer account.'
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponseRedirect('/employer/first_activation/')
    
    else:
        form = SignupForm()
    
    return render(request, 'employer/signup.html', {'form': form})

def first_activation(request):
    return render(request, 'employer/first_activation.html', )

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
#        login(request, user)
        # return redirect('home')

        g = Group.objects.get(name='Employer') 
        g.user_set.add(user)

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#
#
#def signup(request):
#    if request.method == 'POST':
#        form = SignupForm(request.POST)
#        if form.is_valid():
#            user = form.save(commit=False)
#            user.is_active = False
#            user.save()
#            current_site = get_current_site(request)
#            message = render_to_string('acc_active_email.html', {
#                'user':user, 
#                'domain':current_site.domain,
#                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                'token': account_activation_token.make_token(user),
#            })
#            mail_subject = 'Activate your employer account.'
#            to_email = form.cleaned_data.get('email')
#            email = EmailMessage(mail_subject, message, to=[to_email])
#            email.send()
#            return HttpResponse('Please confirm your email address to complete the registration')
#    
#    else:
#        form = SignupForm()
#    
#    return render(request, 'signup.html', {'form': form})
#
#def activate(request, uidb64, token):
#    try:
#        uid = force_text(urlsafe_base64_decode(uidb64))
#        user = User.objects.get(pk=uid)
#    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#        user = None
#    if user is not None and account_activation_token.check_token(user, token):
#        user.is_active = True
#        user.save()
#        login(request, user)
#        # return redirect('home')
#
#        g = Group.objects.get(name='Employer') 
#        g.user_set.add(user)
#
#        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#    else:
#        return HttpResponse('Activation link is invalid!')
#
#def register(request):
#    if request.user.is_authenticated():
#        return redirect(home)
#    registration_form = RegistrationForm()
#    if request.method == 'POST':
#        form = RegistrationForm(request.POST)
#        if form.is_valid():
#            datas={}
#            datas['username']=form.cleaned_data['username']
#            datas['email']=form.cleaned_data['email']
#            datas['password1']=form.cleaned_data['password1']
#
#            #We generate a random activation key
#            usernamesalt1 = datas['username']
#            datas['activation_key']=usernamesalt1
#
#            datas['email_path']="/ActivationEmail.txt"
#            datas['email_subject']="Activation de votre compte yourdomain"
#
#            form.sendEmail(datas)
#            form.save(datas) #Save the user and his profile
#
#            request.session['registered']=True #For display purposes
#            return redirect(home)
#        else:
#            registration_form = form #Display form with error messages (incorrect fields, etc)
#    return render(request, 'employer/register.html', {'form': registration_form})
#
##View called from activation email. Activate user if link didn't expire (48h default), or offer to
##send a second link if the first expired.
#def activation(request, key):
#    activation_expired = False
#    already_active = False
#    profile = get_object_or_404(Profile, activation_key=key)
#    if profile.user.is_active == False:
#        if timezone.now() > profile.key_expires:
#            activation_expired = True #Display: offer the user to send a new activation link
#            id_user = profile.user.id
#        else: #Activation successful
#            profile.user.is_active = True
#            profile.user.save()
#
#    #If user is already active, simply display error message
#    else:
#        already_active = True #Display : error message
#    return render(request, 'employer/activation.html', locals())
#
#def new_activation_link(request, user_id):
#    form = RegistrationForm()
#    datas={}
#    user = User.objects.get(id=user_id)
#    if user is not None and not user.is_active:
#        datas['username']=user.username
#        datas['email']=user.email
#        datas['email_path']="/ResendEmail.txt"
#        datas['email_subject']="Nouveau lien d'activation yourdomain"
#
#        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
#        usernamesalt = datas['username']
#        if isinstance(usernamesalt, unicode):
#            usernamesalt = usernamesalt.encode('utf8')
#        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()
#
#        profile = Profile.objects.get(user=user)
#        profile.activation_key = datas['activation_key']
#        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
#        profile.save()
#
#        form.sendEmail(datas)
#        request.session['new_link']=True #Display: new link sent
#
#    return redirect(home)
