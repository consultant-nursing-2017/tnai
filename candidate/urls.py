from django.conf.urls import url

from . import views

app_name = 'candidate'
urlpatterns = [
    url(r'^candidate_list/', views.IndexView.as_view(), name='index'),
#    url(r'^submit_candidate/', views.submit_candidate, name='submit'),
    url(r'^submit_candidate_personal/', views.submit_candidate_personal, name='submit_candidate_personal'),
    url(r'^submit_candidate_educational_qualifications/', views.submit_candidate_educational_qualifications, name='submit_candidate_educational_qualifications'),
    url(r'^submit_candidate_professional_qualifications/', views.submit_candidate_professional_qualifications, name='submit_candidate_professional_qualifications'),
    url(r'^submit_candidate_additional_qualifications/', views.submit_candidate_additional_qualifications, name='submit_candidate_additional_qualifications'),
    url(r'^submit_candidate_experience/', views.submit_candidate_experience, name='submit_candidate_experience'),
    url(r'^submit_candidate_eligibility_tests/', views.submit_candidate_eligibility_tests, name='submit_candidate_eligibility_tests'),
    url(r'^submit_candidate_snc/', views.submit_candidate_snc, name='submit_candidate_snc'),
    url(r'^submit_candidate_passport/', views.submit_candidate_passport, name='submit_candidate_passport'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
]
