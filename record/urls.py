from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.post_grid, name='grid'),
    url(r'^create/$', views.pres_create, name='create'),
    url(r'^read/$', views.pres_read, name='read'),
    url(r'^print/$', views.pres_print, name='print'),
    url(r'^createskill/$',
        views.skill_create,
        name='skill_create'),
    url(r'^(?P<slug>[\w-]+)/read/$',
        views.skill_read,
        name='skill_read'),
    url(r'^(?P<slug>[\w-]+)/update/$',
        views.skill_update,
        name='skill_update'),
    url(r'^(?P<slug>[\w-]+)/delete/$',
        views.skill_delete,
        name='skill_delete'),
    # url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='edit'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete),
]
