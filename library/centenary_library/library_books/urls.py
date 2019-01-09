from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [

#BOOK_URL's
url(r'^post_book/', views.post_book.as_view(), name='book1'),
url(r'^read_book/', views.read_book.as_view(), name='book2'),
url(r'^update_book/(?P<pk>[0-9]+)/$', views.update_book.as_view(), name='book3'),
url(r'^delete_book/(?P<pk>[0-9]+)/$', views.delete_book.as_view(), name='book4'),
#chapter_url
url(r'^post_chapter/', views.post_chapter.as_view(), name='chapter1'),
url(r'^get_chapter/', views.get_chapter.as_view(), name='chapter2'),
url(r'^put_chapter/(?P<pk>[0-9]+)/$', views.put_chapter.as_view(), name='chapter3'),
url(r'^delete_chapter/(?P<pk>[0-9]+)/$', views.delete_chapter.as_view(), name='chapter4'),
url(r'^bookndchapter_get/(?P<pk>[0-9]+)/$', views.bookndchapter_get.as_view(), name='fullrecord'),
#page_url
url(r'^post_page/', views.post_page.as_view(), name='Page1'),
url(r'^get_page/', views.get_page.as_view(), name='Page2'),
url(r'^put_page/(?P<pk>[0-9]+)/$', views.put_page.as_view(), name='Page3'),
url(r'^delete_page/(?P<pk>[0-9]+)/$', views.delete_page.as_view(), name='Page4'),
url(r'^chapterndpage_get/(?P<pk>[0-9]+)/$', views.chapterndpage_get.as_view(), name='page5')
]