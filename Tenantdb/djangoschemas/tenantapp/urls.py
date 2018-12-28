from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [


    url(r'^studentcreate/', views.student_create.as_view(), name='student_create'),
    url(r'^studentread/', views.student_read.as_view(), name='student_create'),
    url(r'^studentupdate/(?P<pk>[0-9]+)/$', views.student_update.as_view(), name='student_update'),
    url(r'^studentdelete/(?P<pk>[0-9]+)/$', views.student_delete.as_view(), name='student_delete'), 
]