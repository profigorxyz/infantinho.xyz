from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^get_print_url/$',
        views.get_print_url,
        name='get_print_url'),
    url(r'^get_students/$',
        views.get_students,
        name='get_students'),
    url(r'^get_presents/$',
        views.get_presents,
        name='get_students'),
    url(r'^get_achiev/$',
        views.get_achiev,
        name='get_achiev'),
]
