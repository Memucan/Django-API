from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [

    url(r'^school_create/', views.school_create.as_view(), name='school_create'),
    url(r'^school_read/', views.school_read.as_view(), name='school_read'),
    url(r'^school_update/(?P<pk>[0-9]+)/$', views.school_update.as_view(), name='school_update'),
    url(r'^school_delete/(?P<pk>[0-9]+)/$', views.school_delete.as_view(), name='school_delete'), 
]
 