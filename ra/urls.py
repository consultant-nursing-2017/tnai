from django.conf.urls import url

from . import views

app_name = 'ra'
urlpatterns = [
    url(r'^$', views.ra_index, name='index'),
    url(r'^candidate_list/', views.candidate_list, name='candidate_list'),
    url(r'^employer_list/', views.employer_list, name='employer_list'),
    url(r'^advertisement_list/', views.advertisement_list, name='advertisement_list'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
]
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
