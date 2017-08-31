from django.conf.urls import url

from . import views

app_name = 'candidate'
urlpatterns = [
    url(r'^candidate_list/', views.IndexView.as_view(), name='index'),
    url(r'^submit_candidate/', views.submit_candidate, name='submit'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
]
