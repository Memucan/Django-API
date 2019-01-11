from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [ 
    url(r'^sumviewpoet/',  views.view_sumpoet.as_view(), name='getOwner'),
    url(r'^sumviewpoetsec/',  views.view_sumpoetsec.as_view(), name='getOwner'),
    url(r'^tensumviewpoet/',  views.view_tensumpoet.as_view(), name='getOwner'),
    url(r'^tensumviewpoetsec/',  views.view_tensumpoetsec.as_view(), name='getOwner'),
    url(r'^createpoet/',  views.view_createpoet.as_view(), name='getOwner'), 
    url(r'^detviewpoet/(?P<pk>[0-9]+)/$',  views.view_detailpoet.as_view(), name='getOwner'),
    url(r'^pubpoetview/(?P<pk>[0-9]+)/$',  views.view_publicptview.as_view(), name='getOwner'),
    url(r'^updatepoet/(?P<pk>[0-9]+)/$',  views.view_updatepoet.as_view(), name='getOwner'),
    url(r'^deletepoet/(?P<pk>[0-9]+)/$',  views.view_deletepoet.as_view(), name='getOwner'),
    url(r'^poetlike/(?P<pk>[0-9]+)/$',  views.view_poetlikes.as_view(), name='getOwner'),
    url(r'^poetshare/(?P<pk>[0-9]+)/$',  views.view_poetshare.as_view(), name='getOwner'),
    url(r'^getuserrewardhis/(?P<pk>[0-9]+)/$',  views.view_getrewardhisuser.as_view(), name='getOwner'),
    
    url(r'^postcomments/',  views.view_createpoetcomments.as_view(), name='getOwner'),
    url(r'^getcompetition/',  views.view_getcomp.as_view(), name='getOwner'),
    url(r'^getrewardhistiry/',  views.view_paidsumpayment.as_view(), name='getOwner'),
    url(r'^getresult/',  views.view_paidsumwinner.as_view(), name='getOwner'),

    url(r'^createpoetcomplain/',  views.view_createpoetcomplain.as_view(), name='getOwner'), 
    
    url(r'^createnoti/',  views.view_createnotifi.as_view(), name='getOwner'),
    url(r'^viewnoti/(?P<pk>[0-9]+)/$',  views.view_sumviewotifi.as_view(), name='getOwner'),
    url(r'^detviewnoti/(?P<pk>[0-9]+)/$',  views.view_detailotifi.as_view(), name='getOwner'),
    url(r'^updatenoti/(?P<pk>[0-9]+)/$',  views.view_updateotifi.as_view(), name='getOwner'),
    url(r'^deletenoti/(?P<pk>[0-9]+)/$',  views.view_deleteotifi.as_view(), name='getOwner'),
    
    ] 
 
urlpatterns = format_suffix_patterns(urlpatterns)