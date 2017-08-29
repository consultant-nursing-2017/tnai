from django import forms
from django.forms import ModelForm
from .models import Employer
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
    def __init__(self, *args, **kwargs):
        super (SubmitForm,self ).__init__(*args, **kwargs) # populates the post
        self.fields['registration_certification'].required = False
        self.fields['authorized_signatory_id_proof'].required = False
        self.fields['total_employees'].required = False
#        self.fields['authorized_signatory_ID_proof'].required = False
#        self.fields['authorized_signatory_ID_proof'].required = False
#        sponsorsQS = Group.objects.filter(name='Sponsors')
#        self.fields['sponsor'].queryset = User.objects.filter(groups__in=sponsorsQS)
#        contributorsQS = Group.objects.filter(name='Contributors')
#        self.fields['contributor'].queryset = User.objects.filter(groups__in=contributorsQS)

    class Meta:
        model = Employer
        fields = '__all__' #['contributor', 'sponsor', 'url', 'date_submitted', 'approved']
#        widgets={'date_submitted': forms.DateTimeInput(format='%Y-%m-%d %H:%M')}
 


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#class RegistrationForm(forms.Form):
#    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Username','class':'form-control input-perso'}),max_length=30,min_length=3)#,validators=[isValidUsername, validators.validate_slug])
#    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control input-perso'}),max_length=100,error_messages={'invalid': ("Email invalide.")})#,validators=[isValidEmail])
#    password1 = forms.CharField(label="",max_length=50,min_length=6,
#                                widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control input-perso'}))
#    password2 = forms.CharField(label="",max_length=50,min_length=6,
#                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class':'form-control input-perso'}))
#
#    #recaptcha = ReCaptchaField()
#
#    #Override clean method to check password match
#    def clean(self):
#        password1 = self.cleaned_data.get('password1')
#        password2 = self.cleaned_data.get('password2')
#
#        if password1 and password1 != password2:
#            self._errors['password2'] = ErrorList([u"Passwords do not match!"])
#
#        return self.cleaned_data
#
#    #Override of save method for saving both User and Profile objects
#    def save(self, datas):
#        u = User.objects.create_user(datas['username'],
#                                     datas['email'],
#                                     datas['password1'])
#        u.is_active = False
#        u.save()
#        profile=Profile()
#        profile.user=u
#        profile.activation_key=datas['activation_key']
#        profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
#        profile.save()
#        return u
#
#    #Sending activation email ------>>>!! Warning : Domain name is hardcoded below !!<<<------
#    #The email is written in a text file (it contains templatetags which are populated by the method below)
#    def sendEmail(self, datas):
#        link="127.0.0.1:8000/employer/activate/"+datas['activation_key']
#        c=Context({'activation_link':link,'username':datas['username']})
#        f = open(settings.MEDIA_ROOT+datas['email_path'], 'r')
#        t = Template(f.read())
#        f.close()
#        message=t.render(c)
#        #print unicode(message).encode('utf8')
#        send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
