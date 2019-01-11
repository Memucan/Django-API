from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [ 
    

    url(r'^dashboard/',  views.view_dashboard.as_view(), name='getOwner'),
    url(r'^adminlogin/',  views.Vw_User_AdminLogin.as_view(), name='getOwner'),
    url(r'^forgotpass/',  views.Vw_User_ForgotPassword.as_view(), name='getOwner'),
    url(r'^passreset/',  views.reset_Password.as_view(), name='getOwner'),
    
    url(r'^updateadminuser/(?P<pk>[0-9]+)/$',  views.view_updateadmin.as_view(), name='getOwner'),
    url(r'^validadminpass/(?P<pk>[0-9]+)/$',  views.Vw_User_Adminpassw.as_view(), name='getOwner'),
    url(r'^updateadminpass/(?P<pk>[0-9]+)/$',  views.view_updatepass.as_view(), name='getOwner'),
    url(r'^detviewadmin/',  views.view_detview.as_view(), name='getOwner'),
    url(r'^sumviewadmin/',  views.view_sumviewadmin.as_view(), name='getOwner'),

    url(r'^register/',  views.view_createacc.as_view(), name='getOwner'),
    url(r'^sumviewactaccount/',  views.view_actsumacc.as_view(), name='getOwner'),
    url(r'^sumviewinactaccount/',  views.view_inactsumacc.as_view(), name='getOwner'),
    url(r'^detviewaccount/(?P<pk>[0-9]+)/$',  views.view_detailacc.as_view(), name='getOwner'),
    url(r'^updateaccount/(?P<pk>[0-9]+)/$',  views.view_updateacc.as_view(), name='getOwner'),
    url(r'^deleteaccount/(?P<pk>[0-9]+)/$',  views.view_deletacc.as_view(), name='getOwner'),
    url(r'^actorinactaccount/(?P<pk>[0-9]+)/$',  views.view_activeorinavtive.as_view(), name='getOwner'), 

    url(r'^uploadimage/',  views.view_uploadimage.as_view(), name='getOwner'),
    url(r'^getimagepoet/',  views.view_getimagepoet.as_view(), name='getOwner'),
    url(r'^getallimage/',  views.view_getallimage.as_view(), name='getOwner'),
    url(r'^updateimage/(?P<pk>[0-9]+)/$',  views.view_updatimage.as_view(), name='getOwner'),
    url(r'^removeimage/(?P<pk>[0-9]+)/$',  views.view_removeimage.as_view(), name='getOwner'),

    
    url(r'^createcompt/',  views.view_createcomp.as_view(), name='getOwner'),
    url(r'^sumviewcomptupcm/',  views.view_sumcompupcomig.as_view(), name='getOwner'),
    url(r'^sumviewcomptongn/',  views.view_sumcompongng.as_view(), name='getOwner'),
    url(r'^sumviewcomptfinh/',  views.view_sumcompcomp.as_view(), name='getOwner'),
    url(r'^detviewcompt/(?P<pk>[0-9]+)/$',  views.view_detailcompc.as_view(), name='getOwner'),
    url(r'^updatecompt/(?P<pk>[0-9]+)/$',  views.view_updatecomp.as_view(), name='getOwner'),
    url(r'^deletecompt/(?P<pk>[0-9]+)/$',  views.view_deletecomp.as_view(), name='getOwner'),

    
    url(r'^sumviewactcomp/',  views.view_sumviewcomplact.as_view(), name='getOwner'),
    url(r'^sumviewblkcomp/',  views.view_sumviewcomplblk.as_view(), name='getOwner'),
    url(r'^detviewcomp/(?P<pk>[0-9]+)/$',  views.view_complaindetview.as_view(), name='getOwner'),
    url(r'^blockpost/(?P<pk>[0-9]+)/$',  views.view_blkpost.as_view(), name='getOwner'),
    url(r'^unblockpost/(?P<pk>[0-9]+)/$',  views.view_unblkpost.as_view(), name='getOwner'),
    url(r'^deletecomp/(?P<pk>[0-9]+)/$',  views.view_deletecomplaint.as_view(), name='getOwner'),
    

    url(r'^createwin/',  views.view_createwinner.as_view(), name='getOwner'),
    url(r'^paidsumviewwin/',  views.view_paidsumwinner.as_view(), name='getOwner'),
    url(r'^unpaidsumviewwin/',  views.view_unpaidsumwinner.as_view(), name='getOwner'),
    url(r'^detviewwin/(?P<pk>[0-9]+)/$',  views.view_detailwinner.as_view(), name='getOwner'),
    url(r'^updatewin/(?P<pk>[0-9]+)/$',  views.view_updatewinner.as_view(), name='getOwner'),
    url(r'^deletewin/(?P<pk>[0-9]+)/$',  views.view_deletewinner.as_view(), name='getOwner'),

    url(r'^createpayment/',  views.view_createpayment.as_view(), name='getOwner'),
    url(r'^sumviewpayment/',  views.view_paidsumpayment.as_view(), name='getOwner'),
    url(r'^detviewpayment/(?P<pk>[0-9]+)/$',  views.view_detailpayment.as_view(), name='getOwner'),
    url(r'^updatepayment/(?P<pk>[0-9]+)/$',  views.view_updatepayment.as_view(), name='getOwner'),
    url(r'^deletepayment/(?P<pk>[0-9]+)/$',  views.view_deletepayment.as_view(), name='getOwner'),
    
    url(r'^createnoti/',  views.view_createnotifi.as_view(), name='getOwner'),
    url(r'^viewnoti/(?P<pk>[0-9]+)/$',  views.view_sumviewotifi.as_view(), name='getOwner'),
    url(r'^detviewnoti/(?P<pk>[0-9]+)/$',  views.view_detailotifi.as_view(), name='getOwner'),
    url(r'^updatenoti/(?P<pk>[0-9]+)/$',  views.view_updateotifi.as_view(), name='getOwner'),
    url(r'^deletenoti/(?P<pk>[0-9]+)/$',  views.view_deleteotifi.as_view(), name='getOwner'),
    ] 
 
urlpatterns = format_suffix_patterns(urlpatterns)