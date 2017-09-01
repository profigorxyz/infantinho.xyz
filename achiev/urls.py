from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^upfile/$', views.upload_achiev, name='upload'),
]
