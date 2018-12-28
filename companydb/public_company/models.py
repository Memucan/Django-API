from django.db import models

from tenant_schemas.models import TenantMixin

class company(TenantMixin):
    companyname = models.CharField(max_length=100)
    website    = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    address    = models.CharField(max_length=100)

    def __str__(self):
        return self.companyname

    class Meta:
        db_table = "company"


