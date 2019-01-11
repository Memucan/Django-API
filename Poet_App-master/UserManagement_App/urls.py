from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [ 
    
    url(r'^userlogin/',  views.Vw_User_Login.as_view(), name='getOwner'),
    url(r'^usersociallogin/',  views.Vw_User_SoicalLogin.as_view(), name='getOwner'),
    url(r'^forgotpass/',  views.Vw_User_ForgotPassword.as_view(), name='getOwner'),
    url(r'^passreset/',  views.reset_Password.as_view(), name='getOwner'),

    url(r'^register/',  views.view_createacc.as_view(), name='getOwner'),
    url(r'^detviewaccount/(?P<pk>[0-9]+)/$',  views.view_detailacc.as_view(), name='getOwner'),
    url(r'^updateaccount/(?P<pk>[0-9]+)/$',  views.view_updateacc.as_view(), name='getOwner'),
    
    url(r'^profilepost/(?P<pk>[0-9]+)/$',  views.view_profpost.as_view(), name='getOwner'),

    url(r'^getimagepoet/',  views.view_getimagepoet.as_view(), name='getOwner'),
    ] 
 
urlpatterns = format_suffix_patterns(urlpatterns)