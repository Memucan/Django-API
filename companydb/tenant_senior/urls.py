from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [


    url(r'^senior_create/', views.senior_create.as_view(), name='senior_create'),
    url(r'^senior_read/', views.senior_read.as_view(), name='senior_read'),
    url(r'^senior_update/(?P<pk>[0-9]+)/$', views.senior_update.as_view(), name='senior_update'),
    url(r'^senior_delete/(?P<pk>[0-9]+)/$', views.senior_delete.as_view(), name='senior_delete'), 

    url(r'^qualification_create/', views.qualification_create.as_view(), name='qualification_create'),
    url(r'^qualification_read/', views.qualification_read.as_view(), name='qualification_read'),
    url(r'^qualification_update/(?P<pk>[0-9]+)/$', views.qualification_update.as_view(), name='qualification_update'),
    url(r'^qualification_delete/(?P<pk>[0-9]+)/$', views.qualification_delete.as_view(), name='qualification_delete'), 
    url(r'^seniorqual/(?P<pk>[0-9]+)/$', views.seniorqual.as_view(), name='seniorqual'), 
]