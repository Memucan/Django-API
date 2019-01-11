from rest_framework.urlpatterns import format_suffix_patterns
from .import views
from django.conf.urls import url
from django.conf.urls import url, include

urlpatterns = [ 

    url(r'^sumviewcomptongn/',  views.view_sumcompongng.as_view(), name='getOwner'),
    
    ] 
 
urlpatterns = format_suffix_patterns(urlpatterns)