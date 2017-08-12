from django.conf.urls import url

from . import views

app_name = 'candidate'
urlpatterns = [
    url(r'^candidate_list/', views.IndexView.as_view(), name='index'),
    url(r'^submit_candidate/', views.submit_candidate, name='submit'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
]
