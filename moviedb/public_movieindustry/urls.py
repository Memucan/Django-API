from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [

    url(r'^industryname_create/', views.industryname_create.as_view(), name='industryname_create'),
    url(r'^industryname_read/', views.industryname_read.as_view(), name='industryname_read'),
    url(r'^industryname_update/(?P<pk>[0-9]+)/$', views.industryname_update.as_view(), name='industryname_update'),
    url(r'^industryname_update/(?P<pk>[0-9]+)/$', views.industryname_update.as_view(), name='industryname_update'), 
]
 