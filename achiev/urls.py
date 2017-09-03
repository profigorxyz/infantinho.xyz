from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^upfile/$', views.upload_achiev, name='upload'),
    url(r'^read/$',
        views.read_achiev,
        name='read'),
    url(r'^update/$',
        views.evaluate_achiev,
        name='evaluate'),
]
