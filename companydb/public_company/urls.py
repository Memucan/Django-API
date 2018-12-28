from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [

    url(r'^company_create/', views.company_create.as_view(), name='company_create'),
    url(r'^company_read/', views.company_read.as_view(), name='company_read'),
    url(r'^company_update/(?P<pk>[0-9]+)/$', views.company_update.as_view(), name='company_update'),
    url(r'^company_delete/(?P<pk>[0-9]+)/$', views.company_delete.as_view(), name='company_delete'), 
]
 