from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tenant/', include('tenantapp.urls')),
    url(r'^public/', include('publicapp.urls')),
]
