"""infantinho URL Configuration

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
from filebrowser.sites import site
from blog import views as bviews
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^$', bviews.post_grid, name='index'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^record/', include('record.urls', namespace='record')),
    url(r'^herd/', include('herd.urls', namespace='herd')),
    url(r'^achiev/', include('achiev.urls', namespace='achiev')),
    url(r'^ajax/', include('ajax.urls', namespace='ajax')),
    url('', include('social_django.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^terms/$',
        TemplateView.as_view(
            template_name="terms.txt",
            content_type="text/plain"
        ),
        name="terms"),
    url(r'^robots.txt$',
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"),
        name="robots"),
]
