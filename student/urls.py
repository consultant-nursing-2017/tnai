from django.conf.urls import url

from . import views

app_name = 'student'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^entire_profile/', views.index, name='entire_profile'),
    url(r'^submit_student/', views.submit_student, name='submit_student'),
]
