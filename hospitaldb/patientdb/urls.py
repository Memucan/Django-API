from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [

#PatientURL's
url(r'^patient1/', views.patient1.as_view(), name='patient1'),
url(r'^patient2/', views.patient2.as_view(), name='patient2'),
url(r'^patient4/(?P<pk>[0-9]+)/$', views.patient4.as_view(), name='patient4'),
url(r'^patient3/(?P<pk>[0-9]+)/$', views.patient3.as_view(), name='patient3'),

#HospitalURL's
url(r'^hospital1/', views.hospital1.as_view(), name='hospital1'),
url(r'^hospital2/', views.hospital2.as_view(), name='hospital2'),
url(r'^hospital3/(?P<pk>[0-9]+)/$', views.hospital3.as_view(), name='hospital3'),
url(r'^hospital4/(?P<pk>[0-9]+)/$', views.hospital4.as_view(), name='hospital4'),


url(r'^fullrecord/(?P<pk>[0-9]+)/$', views.fullrecord.as_view(), name='fullrecord'),

url(r'^filter1/', views.filter1.as_view(), name='filter1'),
url(r'^filter2/', views.filter2.as_view(), name='filter2'),
url(r'^filter3/', views.filter3.as_view(), name='filter3'),
url(r'^filter4/', views.filter4.as_view(), name='filter4'),

#hospital and patient
url(r'^patienthospitaldata/', views.patienthospitaldata.as_view(), name='patienthospitaldata')


]