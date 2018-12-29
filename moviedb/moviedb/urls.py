from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tenant_moviedetails/', include('tenant_moviedetails.urls')),
]