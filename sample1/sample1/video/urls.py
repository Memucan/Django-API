from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [
    url(r'^postvideo', views.postvideo.as_view(), name='videopost'),
    url(r'getvideo', views.getvideo.as_view(), name='videoget'),
    url(r'getspecificmusic/(?P<pk>[0-9]+)/$', views.getspecificmusic.as_view(), name='getspevideo'),
    url(r'deletevideo/(?P<pk>[0-9]+)/$', views.deletevideo.as_view(), name='delvideo' ),



]

urlpatterns = format_suffix_patterns(urlpatterns)