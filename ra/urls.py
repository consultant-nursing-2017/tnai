from django.conf.urls import url

from . import views

app_name = 'ra'
urlpatterns = [
    url(r'^$', views.ra_index, name='index'),
    url(r'^candidate_list/', views.candidate_list, name='candidate_list'),
    url(r'^show_saved_candidate_lists/', views.show_saved_candidate_lists, name='show_saved_candidate_lists'),
    url(r'^employer_list/', views.employer_list, name='employer_list'),
    url(r'^advertisement_list/', views.advertisement_list, name='advertisement_list'),
    url(r'^filter_candidates/', views.filter_candidates, name='filter_candidates'),
    url(r'^save_list/', views.save_list, name='save_list'),
    url(r'^manipulate_list/', views.manipulate_list, name='manipulate_list'),
    url(r'^generate_list_of_exam_candidates/', views.generate_list_of_exam_candidates, name='generate_list_of_exam_candidates'),
    url(r'^verify_candidate/', views.verify_candidate, name='verify_candidate'),
    url(r'^verify_employer/', views.verify_employer, name='verify_employer'),
    url(r'^edit_list_state_nursing_council/', views.edit_list_state_nursing_council, name='edit_list_state_nursing_council'),
    url(r'^act_as/', views.act_as, name='act_as'),
    url(r'^activate_candidate/', views.activate_candidate, name='activate_candidate'),
    url(r'^delete_user/', views.delete_user, name='delete_user'),
    url(r'^delete_advertisement/', views.delete_advertisement, name='delete_advertisement'),
    url(r'^delete_exam/', views.delete_exam, name='delete_exam'),
#    url(r'^activate_employer/', views.activate_employer, name='activate_employer'),
#    url(r'^$', views.IndexView.as_view(), name='index'),
]
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^submit_to_sponsor/$', views.submit_to_sponsor, name='submit'),
#url(r'^$', views.DetailView.as_view(), name='detail'),
