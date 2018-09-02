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
from instructor.models import Exam, Question, Answer
from .models import Student, TakeExam
from .forms import StudentForm, TakeExamForm, ShowQuestionInExamForm
#from .forms import RegistrationForm
from django.core.mail import send_mail
import hashlib
import random
import pdb
from django.utils.crypto import get_random_string
from django.contrib import auth

from django.shortcuts import render, redirect
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

def is_student_user(username, request):
    student_user = True
    if username.groups.filter(name="Student").count() <= 0:
        student_user = False
    
    return student_user

def is_allowed(username, request):
    allowed = is_student_user(username, request)
    return allowed

def get_acting_user(request):
    username=auth.get_user(request)
    return username

def index(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    object_does_not_exist = False
    if username.groups.filter(name="Candidate").count() > 0:
        return HttpResponseRedirect('/candidate/')

    try:
        if username.is_authenticated():
            student = Student.objects.get(username=username)
        else:
            student = None
    except ObjectDoesNotExist:
        student = None
        object_does_not_exist = True

    return render(request, 'student/index.html', {'student': student, 'object_does_not_exist': object_does_not_exist, }) 

def submit_student(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    new_profile = True
    if request.method == 'POST':
        # check whether it's valid:
        # TODO

        try:
            student = Student.objects.get(username=username)
            new_profile = False
            form = StudentForm(request.POST, request.FILES, instance=student)
        except ObjectDoesNotExist:
            new_profile = True
            form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/student/')
    else:
        # if a GET (or any other method) we'll create a blank form
        try:
            student = Student.objects.get(username=username)
            form = StudentForm(instance=student)
            new_profile = False
        except ObjectDoesNotExist:
            new_profile = True
            form = StudentForm(initial={'username': username,})

    return render(request, 'student/submit_student.html', {'new_profile': new_profile, 'form': form,}) 

def choose_exam(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    if request.method == 'POST':
        form = TakeExamForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save()
            exam = form.cleaned_data['exam']
            return HttpResponseRedirect('/student/take_exam/?exam_id=' + str(exam.exam_id))
    else:
        # if a GET (or any other method) we'll create a blank form
        form = TakeExamForm()

    return render(request, 'student/choose_exam.html', {'form': form, }) 

def take_exam(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    exam_id = None
    take_exam = None
    if request.method == 'POST':
        try:
            if 'exam_id' in request.POST:
                exam_id = request.POST.get('exam_id')
                exam = Exam.objects.get(exam_id = exam_id)
                take_exam = TakeExam.objects.get(exam = exam)
                form = ShowQuestionInExamForm(request.POST, request.FILES, instance = take_exam)
            else:
                return render(request, 'student/not_allowed.html', {'next': request.path})
        except ObjectDoesNotExist:
            return render(request, 'student/not_allowed.html', {'next': request.path})

        if form.is_valid():
            instance = form.save(commit = False)
            answer = form.cleaned_data['answer']
            instance.answers_given.add(answer)
            instance.current_question = instance.current_question + 1
            instance.save()
            if instance.current_question >= instance.exam.questions.count():
                instance.completed = True
                instance.completion_time = timezone.now()
            form.save()

            if instance.completed:
                return HttpResponseRedirect('/student/')
            else:
                return HttpResponseRedirect('/student/take_exam/?exam_id=' + exam_id)
    else:
        # if a GET (or any other method) we'll create a blank form
        if 'exam_id' in request.GET:
            exam_id = request.GET.get('exam_id')
            exam = Exam.objects.get(exam_id = exam_id)
            take_exam = TakeExam.objects.get(exam = exam)
            if take_exam.current_question >= take_exam.exam.questions.count():
                return HttpResponseRedirect('/student/')
            else:
                form = ShowQuestionInExamForm(instance = take_exam)
        else:
            return render(request, 'student/not_allowed.html', {'next': request.path})

    question = take_exam.exam.questions.all()[take_exam.current_question]
    return render(request, 'student/take_exam.html', {'form': form, 'exam_id': exam_id, 'question': question}) 

def exam_history(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    queryset = TakeExam.objects.filter(completed = True)
    return render(request, 'student/exam_history.html', {'queryset': queryset, })

def exam_result(request):
    username = get_acting_user(request)
    allowed = is_allowed(username, request)
    if not allowed:
        return render(request, 'student/not_allowed.html', {'next': request.path})

    exam_id = None
    take_exam = None

    if request.method == 'GET':
        if 'exam_id' in request.GET:
            exam_id = request.GET.get('exam_id')
            exam = Exam.objects.get(exam_id = exam_id)
            take_exam = TakeExam.objects.get(exam = exam)
            answers_given = take_exam.answers_given.all()
            question_queryset = exam.questions.all()
            values = []
            count_question = 1
            for question in question_queryset:
                question_answer_pair = [question, []]
                answer_queryset = Answer.objects.filter(question = question).order_by('text')
                count_answer = 0
                for answer in answer_queryset:
                    answer_key = 0
                    if answer.correct:
                        answer_key = answer_key + 1
                    if answer in answers_given:
                        answer_key = answer_key + 2
                    question_answer_pair[1].append([answer, answer_key])
                    count_answer = count_answer + 1

                values.append([count_question, question_answer_pair])
                count_question = count_question + 1
    else:
        return HttpResponseRedirect('/student/')

    return render(request, 'student/exam_result.html', {'values': values}) 
