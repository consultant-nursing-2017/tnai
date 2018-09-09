from django.conf.urls import url

from . import views

app_name = 'student'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^entire_profile/', views.index, name='entire_profile'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^submit_student/', views.submit_student, name='submit_student'),
    url(r'^choose_exam/', views.choose_exam, name='choose_exam'),
    url(r'^take_exam/', views.take_exam, name='take_exam'),
    url(r'^exam_result/', views.exam_result, name='exam_result'),
    url(r'^exam_history/', views.exam_history, name='exam_history'),
]
