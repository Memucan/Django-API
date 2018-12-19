from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [

    url(r'^studentpost/', views.studentpost.as_view(), name='studentpost'),
    url(r'^studentget/', views.studentget.as_view(), name='studentget'),
    url(r'^studentdelete/(?P<pk>[0-9]+)/$', views.studentdelete.as_view(), name='studentdelete'),
    url(r'^studentupdate/(?P<pk>[0-9]+)/$', views.studentupdate.as_view(), name='studentupdate'),

#FEES
    url(r'^feepost/', views.feepost.as_view(), name='feepost'),
    url(r'^feesget/', views.feesget.as_view(), name='feesget'),
    url(r'^studentandfees/(?P<pk>[0-9]+)/$', views.studentandfees.as_view(), name='studentandfees'), 
    url(r'^getstudent/', views.studentfilter.as_view(), name='feesget'),
   
#FILTERS   
    url(r'^studentFilter1/', views.studentFilter1.as_view(), name='studentFilter1'),
    url(r'^studentfilter2/', views.studentfilter2.as_view(), name='studentfilter2'),
    url(r'^studentfilter3/', views.studentfilter3.as_view(), name='studentfilter3'),
    url(r'^studentfilter4/', views.studentfilter4.as_view(), name='studentfilter4'),
    url(r'^studentfilter5/', views.studentfilter5.as_view(), name='studentfilter5'),
    url(r'^studentFilter6/', views.studentFilter6.as_view(), name='studentFilter6'),
    url(r'^studentfilter7/', views.studentfilter7.as_view(), name='studentfilter7'),
    




]