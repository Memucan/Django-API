from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [


    url(r'^employee_create/', views.employee_create.as_view(), name='employee_create'),
    url(r'^employee_read/', views.employee_read.as_view(), name='employee_read'),
    url(r'^employee_update/(?P<pk>[0-9]+)/$', views.employee_update.as_view(), name='employee_update'),
    url(r'^employee_delete/(?P<pk>[0-9]+)/$', views.employee_delete.as_view(), name='employee_delete'), 

    url(r'^leave_create/', views.leave_create.as_view(), name='leave_create'),
    url(r'^leave_read/', views.leave_read.as_view(), name='leave_read'),
    url(r'^leave_update/(?P<pk>[0-9]+)/$', views.leave_update.as_view(), name='leave_update'),
    url(r'^leave_delete/(?P<pk>[0-9]+)/$', views.leave_delete.as_view(), name='leave_delete'), 
    url(r'^leave_getuser/(?P<pk>[0-9]+)/$', views.leave_getuser.as_view(), name='leave_getuser'),
]