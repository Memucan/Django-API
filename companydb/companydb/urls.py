from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tenant_employee/', include('tenant_employee.urls')),
    url(r'^tenant_senior/', include('tenant_senior.urls')), 
]
