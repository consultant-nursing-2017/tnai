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
from .models import Instructor, Topic, Question, Answer, QuestionBank, Exam
from .forms import InstructorForm, TopicForm, QuestionForm, AnswerForm, QuestionBankForm, ExamForm
#from .forms import RegistrationForm
from django.core.mail import send_mail
import hashlib
import random
import pdb
from django.utils.crypto import get_random_string
from django.contrib import auth

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
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

class IndexView(generic.ListView):
    template_name = 'employer/index.html'
    context_object_name = 'employer_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Employer.objects.all()

def is_student_user(username, request):
    student_user = True
    if username.groups.filter(name="Student").count() <= 0:
        student_user = False
    
    return student_user

def is_instructor_user(username, request):
    instructor_user = True
    if username.groups.filter(name="Instructor").count() <= 0:
        instructor_user = False
    
    return instructor_user

def is_allowed(username, request):
    allowed = is_instructor_user(username, request)
    return allowed

def get_acting_user(request):
    username=auth.get_user(request)
    return username

def index(request):
    username = get_acting_user(request)
    if username.groups.filter(name="Student").count() > 0:
        return HttpResponseRedirect('/student/')

    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    object_does_not_exist = False
    if username.groups.filter(name="Student").count() > 0:
        return HttpResponseRedirect('/Student/')

    try:
        if username.is_authenticated():
            instructor = Instructor.objects.get(username=username)
        else:
            instructor = None
    except ObjectDoesNotExist:
        instructor = None
        object_does_not_exist = True

    return render(request, 'instructor/index.html', {'instructor': instructor, 'object_does_not_exist': object_does_not_exist, }) 

def submit_instructor(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    new_profile = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            instructor = Instructor.objects.get(username=username)
            new_profile = False
            form = InstructorForm(request.POST, request.FILES, instance=instructor)
        except ObjectDoesNotExist:
            new_profile = True
            form = InstructorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/instructor/')
    else:
        # if a GET (or any other method) we'll create a blank form
        try:
            instructor = Instructor.objects.get(username=username)
            form = InstructorForm(instance=instructor)
            new_profile = False
        except ObjectDoesNotExist:
            new_profile = True
            form = InstructorForm(initial={'username': username,})

    return render(request, 'instructor/submit_instructor.html', {'new_profile': new_profile, 'form': form,}) 

def submit_question_bank(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    question_bank_id = None
    if request.method == 'POST':
        try:
            if 'question_bank_id' in request.POST:
                question_bank_id = request.POST.get('question_bank_id')
                question_bank = QuestionBank.objects.get(question_bank_id = question_bank_id)
                form = QuestionBankForm(request.POST, request.FILES, instance = question_bank)
            else:
                form = QuestionBankForm(request.POST, request.FILES)
        except ObjectDoesNotExist:
            form = QuestionBankForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/instructor/')
    else:
        # if a GET (or any other method) we'll create a blank form
        if 'question_bank_id' in request.GET:
            question_bank_id = request.GET.get('question_bank_id')
            question_bank = QuestionBank.objects.get(question_bank_id = question_bank_id)
            form = QuestionBankForm(instance = question_bank)
        else:
            form = QuestionBankForm()

    return render(request, 'instructor/submit_question_bank.html', {'form': form, 'question_bank_id': question_bank_id}) 

def submit_topic(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
#            pdb.set_trace()
#            if 'add_topic' in request.POST:
            form.save()
            return HttpResponseRedirect('/instructor/')
    else:
        # if a GET (or any other method) we'll create a blank form
        form = TopicForm()

    return render(request, 'instructor/submit_topic.html', {'form': form,}) 

def submit_question(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    question_id = None
    if request.method == 'POST':
        try:
            if 'question_id' in request.POST:
                question_id = request.POST.get('question_id')
                question = Question.objects.get(question_id = question_id)
                form = QuestionForm(request.POST, request.FILES, instance = question)
            else:
                form = QuestionForm(request.POST, request.FILES)
        except ObjectDoesNotExist:
            form = QuestionForm(request.POST, request.FILES)

        if form.is_valid():
#            pdb.set_trace()
#            if 'add_topic' in request.POST:
            instance = form.save()
            return HttpResponseRedirect('/instructor/submit_answer?question_id=' + str(instance.question_id))
    else:
        # if a GET (or any other method) we'll create a blank form
        if 'question_id' in request.GET:
            question_id = request.GET.get('question_id')
            question = Question.objects.get(question_id = question_id)
            form = QuestionForm(instance = question)
        else:
            form = QuestionForm()

    return render(request, 'instructor/submit_question.html', {'form': form, 'question_id': question_id, }) 

def submit_exam(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    exam_id = None
    if request.method == 'POST':
        try:
            if 'exam_id' in request.POST:
                exam_id = request.POST.get('exam_id')
                exam = Exam.objects.get(exam_id = exam_id)
                form = ExamForm(request.POST, request.FILES, instance = exam)
            else:
                form = ExamForm(request.POST, request.FILES)
        except ObjectDoesNotExist:
            form = ExamForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect('/instructor/')
    else:
        # if a GET (or any other method) we'll create a blank form
        if 'exam_id' in request.GET:
            exam_id = request.GET.get('exam_id')
            exam = Exam.objects.get(exam_id = exam_id)
            form = ExamForm(instance = exam)
        else:
            form = ExamForm()

    return render(request, 'instructor/submit_exam.html', {'form': form, 'exam_id': exam_id, }) 

def submit_answer(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    question_id = None
    if request.method == 'GET':
        if 'question_id' in request.GET:
            question_id = request.GET.__getitem__('question_id')
        else:
            return render(request, 'exam/exam_id_not_found.html', {'question_id': question_id, })
    else:
        if 'question_id' in request.POST:
            question_id = request.POST.get('question_id', "")
        else:
            return render(request, 'exam/exam_id_not_found.html', {'question_id': question_id, })

    try:
        question = Question.objects.get(question_id = question_id)
        queryset = Answer.objects.filter(question = question)
        extra_forms = 1
        AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=extra_forms, can_delete=True)

    except ObjectDoesNotExist:
        return render(request, 'exam/exam_id_not_found.html', {'question_id': question_id, })
#        return HttpResponseRedirect('/instructor/')

    if request.method == 'POST':
        formset = AnswerFormSet(request.POST, request.FILES, instance = question, )
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/instructor/')
    else:
        formset = AnswerFormSet(instance = question, queryset = queryset, )

    form = formset[0]
#    pdb.set_trace()
    return render(request, 'instructor/submit_answer.html', {'formset': formset, 'form': form, 'question_id': question_id, 'question': question, }) 

def list_questions(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    queryset = Question.objects.all()
    return render(request, 'instructor/question_list.html', {'queryset': queryset, }, )

def list_question_banks(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    queryset = QuestionBank.objects.all()
    return render(request, 'instructor/question_bank_list.html', {'queryset': queryset, }, )

def display_all_questions(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request) or is_student_user(username, request)
    allowed = True
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    question_queryset = Question.objects.exclude(text__iexact='')
    exam = None
#    pdb.set_trace()
    if request.method == 'GET':
        try:
            exam_id = request.GET.get('exam_id')
            exam = Exam.objects.get(exam_id = exam_id)
            question_queryset = exam.questions.all()
        except KeyError:
            pass
        except ObjectDoesNotExist:
            pass
    question_queryset = question_queryset.order_by('question_id')
    values = []
    count_question = 1
    answer_format = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)']
    display_answers = not is_student_user(username, request)
    for question in question_queryset:
        question_answer_pair = [question, []]
        answer_queryset = Answer.objects.filter(question = question).order_by('text')
        count_answer = 0
        for answer in answer_queryset:
            question_answer_pair[1].append([answer_format[count_answer], answer])
#            question_answer_pair[1].append(answer)
            count_answer = count_answer + 1

        values.append([count_question, question_answer_pair])
        count_question = count_question + 1
    
    return render(request, 'instructor/display_all_questions.html', {'values': values, 'display_answers': display_answers, }, )

def list_exams(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'instructor/not_allowed.html', {'next': request.path})

    queryset = Exam.objects.all()
    return render(request, 'instructor/exam_list.html', {'queryset': queryset, }, )

def full_question(request):
    pass

#def entire_profile(request):
#    username = get_acting_user(request)
#    allowed = is_allowed(username, request)
#    if not allowed:
#        return render(request, 'employer/not_allowed.html', {'next': request.path})
#    actual_user = auth.get_user(request)
#    ra_user = is_ra_user(actual_user, request)
#
#    try:
#        if 'registration_number' in request.GET:
#            registration_number = request.GET.__getitem__('registration_number')
#            employer = Employer.objects.get(registration_number=registration_number)
#            if not is_ra_user(username, request) and employer.employer_username != username:
#                return render(request, 'employer/not_allowed.html', {'next': request.path}, )
#        else:
#            employer = Employer.objects.get(employer_username=username)
#        employer = Employer.objects.get(employer_username=username)
#        form = EmployerForm()
#        fields_part1 = EmployerForm.fields_part1()
#        fields_part2 = EmployerForm.fields_part2()
#
#        data_part1 = []
#        for field in fields_part1:
#            data_part1.append((form.fields[field].label, getattr(employer, field)))
#
#        data_part2 = []
#        for field in fields_part2:
#            data_part2.append((form.fields[field].label, getattr(employer, field)))
#
#    #    pdb.set_trace()
#
#        registration_number_raw = employer.registration_number
#        registration_number = registration_number_raw.hashid
#        is_provisional_registration_number = getattr(employer, 'is_provisional_registration_number')
#        displayed_registration_number = employer.registration_number_display()
#
#        if employer.sent_email_notification_provisional_registration_number is False:
#            current_site = get_current_site(request)
#            user = employer.employer_username
#            message = render_to_string('employer/provisional_registration_number_email.html', {
#                'user':user, 
#                'domain':current_site.domain,
#                'registration_number_display': employer.registration_number_display()
#            })
#            mail_subject = 'Your provisional TNAI recruitment registration number'
#            to_email = employer.employer_username.username
#            email = EmailMessage(mail_subject, message, to=[to_email])
#            result = email.send()
#            if result:
#                employer.sent_email_notification_provisional_registration_number = True
#                employer.save()
#
##        pdb.set_trace()
#        return render(request, 'employer/entire_profile.html', {'employer': employer, 'fields_part1': fields_part1, 'data_part1': data_part1, 'fields_part2': fields_part2, 'data_part2': data_part2, 'registration_number': registration_number, 'displayed_registration_number': displayed_registration_number, 'ra_user': ra_user, })
#
#    except ObjectDoesNotExist:
#        fields = None
#        return render(request, 'employer/index.html', {'employer': None})
#
#def submit_advertisement(request):
#    username = get_acting_user(request)
#    allowed = is_allowed(username, request)
#    if not allowed:
#        return render(request, 'employer/not_allowed.html', {'next': request.path})
#
#    if not is_employer_user(username, request):
#        return render(request, 'employer/not_allowed.html', {'next': request.path})
#
#    employer = Employer.objects.get(employer_username=username)
#    new_advertisement = True
#    advertisement_id = None
#
#    if request.method == 'GET':
##        pdb.set_trace()
#        if 'advertisement_id' in request.GET:
#            advertisement_id = request.GET.__getitem__('advertisement_id')
#            try:
#                advertisement = Advertisement.objects.filter(employer_advert=employer).get(obfuscated_id=advertisement_id)
#            except ObjectDoesNotExist:
#                return render(request, 'employer/invalid_advertisement_id.html', {'advertisement_id': advertisement_id}, )
#            new_advertisement = False
#            form = AdvertisementForm(instance=advertisement)
#        else:
#            advertisement_id = None
#            form = AdvertisementForm(initial={'employer_advert':employer})
#    else:
#        # check whether it's valid:
#        # TODO
#        new_advertisement = (request.POST.get('new_advertisement') == "True")
#        if not new_advertisement:
#            advertisement_id = request.POST.get('advertisement_id')
#            try:
#                advertisement = Advertisement.objects.get(obfuscated_id=advertisement_id)
#            except ObjectDoesNotExist:
#                return render(request, 'employer/invalid_advertisement_id.html', {'advertisement_id': advertisement_id}, )
#            form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
#        else:
#            form = AdvertisementForm(request.POST, request.FILES)
#
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect('/employer/list_advertisements/')
#
#    return render(request, 'employer/submit_advertisement.html', {'new_advertisement': new_advertisement, 'form': form, 'advertisement_id': advertisement_id }) 
#
#def list_advertisements(request):
#    username = get_acting_user(request)
#    allowed = is_allowed(username, request)
#    if not allowed:
#        return render(request, 'employer/not_allowed.html', {'next': request.path})
#
#    employer = Employer.objects.get(employer_username=username)
#    queryset = Advertisement.objects.filter(employer_advert=employer)
#    return render(request, 'ra/advertisement_list.html', {'queryset': queryset, 'employer_restricted': True}, )
#
#def full_advertisement(request):
##    allowed = is_allowed(username, request) or is_candidate_user
##    if not allowed:
##        return render(request, 'employer/not_allowed.html', {'next': request.path})
#
#    username = get_acting_user(request)
#    advertisement_id = None
#    try:
#        advertisement_id = request.GET.__getitem__('advertisement_id')
#    except ObjectDoesNotExist:
#        return render(request, 'employer/invalid_advertisement_id.html', {'advertisement_id': advertisement_id}, )
#    advertisement = Advertisement.objects.get(obfuscated_id=advertisement_id)
#
#    form = AdvertisementForm()
#    full_advertisement = is_verified_candidate_user(username, request) or is_allowed(username, request)
#    if full_advertisement:
#        fields = form.get_fields()
#    else:
#        fields = ['job_role', 'closing_date', 'gender', 'number_of_vacancies', 'educational_qualifications', 'eligibility_tests', 'experience', 'country', 'salary_number', 'salary_currency']
#
#    data_full = []
#    for field in fields:
#        (label, value) = (form.fields[field].label, getattr(advertisement, field))
#        if isinstance(value, bool):
#            if value is False:
#                pass
#        else:
#            data_full.append((label, value))
#
##    pdb.set_trace()
#
#    return render(request, 'employer/full_advertisement.html', {'fields': fields, 'data_full': data_full, 'full_advertisement': full_advertisement})
#
#class DetailView(generic.DetailView):
#    model = Employer
#    template_name = 'employer/detail.html'
#    def get_queryset(self):
#        """
#        Excludes any questions that aren't published yet.
#        """
#        return Employer.objects.all()
#
#def signup(request):
#    if request.method == 'POST':
#        form = SignupForm(request.POST)
#        if form.is_valid():
#            user = form.save(commit=False)
#            user.is_active = False
#            user.save()
#            current_site = get_current_site(request)
#            message = render_to_string('employer/acc_active_email.html', {
#                'user':user, 
#                'domain':current_site.domain,
#                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                'token': account_activation_token.make_token(user),
#            })
#            mail_subject = 'Activate your employer account.'
#            to_email = form.cleaned_data.get('username')
#            email = EmailMessage(mail_subject, message, to=[to_email])
#            email.send()
#            return HttpResponseRedirect('/employer/first_activation/')
#    
#    else:
#        form = SignupForm()
#    
#    return render(request, 'employer/signup.html', {'form': form})
#
#def first_activation(request):
#    return render(request, 'employer/first_activation.html', )
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
##        login(request, user)
#        # return redirect('home')
#
#        g = Group.objects.get(name='Employer') 
#        g.user_set.add(user)
#
#        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#    else:
#        return HttpResponse('Activation link is invalid!')
#
##
##
##def signup(request):
##    if request.method == 'POST':
##        form = SignupForm(request.POST)
##        if form.is_valid():
##            user = form.save(commit=False)
##            user.is_active = False
##            user.save()
##            current_site = get_current_site(request)
##            message = render_to_string('acc_active_email.html', {
##                'user':user, 
##                'domain':current_site.domain,
##                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
##                'token': account_activation_token.make_token(user),
##            })
##            mail_subject = 'Activate your employer account.'
##            to_email = form.cleaned_data.get('email')
##            email = EmailMessage(mail_subject, message, to=[to_email])
##            email.send()
##            return HttpResponse('Please confirm your email address to complete the registration')
##    
##    else:
##        form = SignupForm()
##    
##    return render(request, 'signup.html', {'form': form})
##
##def activate(request, uidb64, token):
##    try:
##        uid = force_text(urlsafe_base64_decode(uidb64))
##        user = User.objects.get(pk=uid)
##    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
##        user = None
##    if user is not None and account_activation_token.check_token(user, token):
##        user.is_active = True
##        user.save()
##        login(request, user)
##        # return redirect('home')
##
##        g = Group.objects.get(name='Employer') 
##        g.user_set.add(user)
##
##        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
##    else:
##        return HttpResponse('Activation link is invalid!')
##
##def register(request):
##    if request.user.is_authenticated():
##        return redirect(home)
##    registration_form = RegistrationForm()
##    if request.method == 'POST':
##        form = RegistrationForm(request.POST)
##        if form.is_valid():
##            datas={}
##            datas['username']=form.cleaned_data['username']
##            datas['email']=form.cleaned_data['email']
##            datas['password1']=form.cleaned_data['password1']
##
##            #We generate a random activation key
##            usernamesalt1 = datas['username']
##            datas['activation_key']=usernamesalt1
##
##            datas['email_path']="/ActivationEmail.txt"
##            datas['email_subject']="Activation de votre compte yourdomain"
##
##            form.sendEmail(datas)
##            form.save(datas) #Save the user and his profile
##
##            request.session['registered']=True #For display purposes
##            return redirect(home)
##        else:
##            registration_form = form #Display form with error messages (incorrect fields, etc)
##    return render(request, 'employer/register.html', {'form': registration_form})
##
###View called from activation email. Activate user if link didn't expire (48h default), or offer to
###send a second link if the first expired.
##def activation(request, key):
##    activation_expired = False
##    already_active = False
##    profile = get_object_or_404(Profile, activation_key=key)
##    if profile.user.is_active == False:
##        if timezone.now() > profile.key_expires:
##            activation_expired = True #Display: offer the user to send a new activation link
##            id_user = profile.user.id
##        else: #Activation successful
##            profile.user.is_active = True
##            profile.user.save()
##
##    #If user is already active, simply display error message
##    else:
##        already_active = True #Display : error message
##    return render(request, 'employer/activation.html', locals())
##
##def new_activation_link(request, user_id):
##    form = RegistrationForm()
##    datas={}
##    user = User.objects.get(id=user_id)
##    if user is not None and not user.is_active:
##        datas['username']=user.username
##        datas['email']=user.email
##        datas['email_path']="/ResendEmail.txt"
##        datas['email_subject']="Nouveau lien d'activation yourdomain"
##
##        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
##        usernamesalt = datas['username']
##        if isinstance(usernamesalt, unicode):
##            usernamesalt = usernamesalt.encode('utf8')
##        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()
##
##        profile = Profile.objects.get(user=user)
##        profile.activation_key = datas['activation_key']
##        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
##        profile.save()
##
##        form.sendEmail(datas)
##        request.session['new_link']=True #Display: new link sent
##
##    return redirect(home)
