from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.views.generic import RedirectView

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^recruitment/', RedirectView.as_view(url="/accounts/login/"), name='recruitment'),
    url(r'^contact/', RedirectView.as_view(url="http://tnaionline.org/news/contactus/"), name='contact'),
    url(r'^media/', RedirectView.as_view(url="http://tnaionline.org/photos/41048-10-photo-gallery.html"), name='media'),
]
