from django.db import models

from tenant_schemas.models import TenantMixin

class school(TenantMixin):
    schoolname = models.CharField(max_length=100)
    branch     = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    address    = models.CharField(max_length=100)

    def __str__(self):
        return self.schoolname

    class Meta:
        db_table = "school"


