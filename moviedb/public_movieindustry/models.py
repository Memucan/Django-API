from django.db import models
from tenant_schemas.models import TenantMixin

class industryname(TenantMixin):
    movieindustryname = models.CharField(max_length=100)
    website    = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
   

    def __str__(self):
        return self.movieindustryname

    class Meta:
        db_table = "industryname_table"


