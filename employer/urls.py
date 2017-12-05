from django.conf.urls import url

from . import views

app_name = 'employer'
urlpatterns = [
    url(r'^$', views.employer_index, name='index'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^submit_employer/', views.submit_employer, name='submit_employer'),
    url(r'^entire_profile/', views.entire_profile, name='entire_profile'),
    url(r'^submit_advertisement/', views.submit_advertisement, name='submit_advertisement'),
    url(r'^list_advertisements/', views.list_advertisements, name='list_advertisements'),
    url(r'^full_advertisement/', views.full_advertisement, name='full_advertisement'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^first_activation/$', views.first_activation, name='first_activation'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
