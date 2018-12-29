from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [


    url(r'^movie_create/', views.movie_create.as_view(), name='movie_create'),
    url(r'^movie_read/', views.movie_read.as_view(), name='movie_read'),
    url(r'^movie_update/(?P<pk>[0-9]+)/$', views.movie_update.as_view(), name='movie_update'),
    url(r'^movie_delete/(?P<pk>[0-9]+)/$', views.movie_delete.as_view(), name='movie_delete'), 

    url(r'^cast_create/', views.cast_create.as_view(), name='cast_create'),
    url(r'^cast_read/', views.cast_read.as_view(), name='cast_read'),
    url(r'^cast_update/(?P<pk>[0-9]+)/$', views.cast_update.as_view(), name='cast_update'),
    url(r'^cast_delete/(?P<pk>[0-9]+)/$', views.cast_delete.as_view(), name='cast_delete'), 

    url(r'^moviecast/(?P<pk>[0-9]+)/$', views.moviecast.as_view(), name='moviecast'),
    url(r'^post_moviecast/', views.post_moviecast.as_view(), name='post_moviecast'),
]