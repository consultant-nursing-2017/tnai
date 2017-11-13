from django.conf.urls import url

from . import views

app_name = 'exam'
urlpatterns = [
    url(r'^$', views.exam_list, name='exam_list'),
    url(r'^exam_list/', views.exam_list, name='exam_list'),
    url(r'^submit_exam/', views.submit_exam, name='submit_exam'),
    url(r'^submit_exam_time_slot/', views.submit_exam_time_slot, name='submit_exam_time_slot'),
#    url(r'^employer_list/', views.employer_list, name='employer_list'),
#    url(r'^advertisement_list/', views.advertisement_list, name='advertisement_list'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
]
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
