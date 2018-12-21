from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [ 
    url(r'^createuser/(?P<pk>[0-9]+)/$',  views.view_music.as_view(), name='getOwner'),
    url(r'^viewuser/',  views.view_music1.as_view(), name='getOwner'),
    url(r'^getmusic/(?P<pk>[0-9]+)/$', views.getmusic.as_view(), name='get_music'),
    url(r'^updatemusic/(?P<pk>[0-9]+)/$', views.updatemusic.as_view(), name='update_music'),
    url(r'^deletemusic/(?P<pk>[0-9]+)/$', views.deletemusic.as_view(), name='delete_music')
    ] 
 
urlpatterns = format_suffix_patterns(urlpatterns)
