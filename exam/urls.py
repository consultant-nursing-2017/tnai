from django.conf.urls import url

from . import views

app_name = 'exam'
urlpatterns = [
    url(r'^$', views.exam_list, name='index'),
    url(r'^show_exam_details/', views.show_exam_details, name='show_exam_details'),
    url(r'^exam_list/', views.exam_list, name='exam_list'),
    url(r'^submit_exam/', views.submit_exam, name='submit_exam'),
    url(r'^submit_exam_time_slot/', views.submit_exam_time_slot, name='submit_exam_time_slot'),
    url(r'^candidate_book_time_slot/', views.candidate_book_time_slot, name='candidate_book_time_slot'),
    url(r'^candidate_show_hall_ticket/', views.candidate_show_hall_ticket, name='candidate_show_hall_ticket'),
]
