from django.conf.urls import url

from . import views

app_name = 'instructor'
urlpatterns = [
    url(r'^$', views.index, name='index'),
##    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^submit_instructor/', views.submit_instructor, name='submit_instructor'),
    url(r'^submit_topic/', views.submit_topic, name='submit_topic'),
    url(r'^submit_question/', views.submit_question, name='submit_question'),
    url(r'^submit_answer/', views.submit_answer, name='submit_answer'),
    url(r'^entire_profile/', views.index, name='entire_profile'),
    url(r'^list_questions/', views.list_questions, name='list_questions'),
    url(r'^display_all_questions/', views.display_all_questions, name='display_all_questions'),
#    url(r'^full_question/', views.submit_answer, name='full_question'),
#    url(r'^submit_advertisement/', views.submit_advertisement, name='submit_advertisement'),
#    url(r'^list_advertisements/', views.list_advertisements, name='list_advertisements'),
#    url(r'^full_advertisement/', views.full_advertisement, name='full_advertisement'),
#    url(r'^signup/$', views.signup, name='signup'),
#    url(r'^first_activation/$', views.first_activation, name='first_activation'),
#    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#        views.activate, name='activate'),
]
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
