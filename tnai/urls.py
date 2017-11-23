"""tnai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^employer/', include('employer.urls')),
    url(r'^candidate/', include('candidate.urls')),
    url(r'^ra/', include('ra.urls')),
    url(r'^exam/', include('exam.urls'), name="exam"),
    url(r'^interview/', RedirectView.as_view(url="/exam/"), name="interview"),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^accounts/profile/', RedirectView.as_view(url="/candidate/"), name="profile"),
    url(r'^accounts/', include('django.contrib.auth.urls'), name="accounts"),
    url(r'^$', RedirectView.as_view(url="/home/")),
    url(r'^home/', include('home.urls'), name="home"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
