from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^upfile/$', views.upload_file, name='upload'),
    url(r'^upgrade/$', views.update_grade, name='upgrade'),
]
