from django.db import models

class patient(models.Model):
    PatientName = models.CharField(max_length=100)
    DOB         = models.DateField(null=True)
    Sex         = models.CharField(max_length=100)
    Occupation  = models.CharField(max_length=100)
    MaritalStatus = models.CharField(max_length=100)
    SpouseName = models.CharField(max_length=100, null=True)
    ContactNumber = models.IntegerField(max_length=20)

    def __str__(self):
        return self.PatientName

    class Meta:
        db_table = "patientbase"     

class hospital(models.Model):
    Illness = models.CharField(max_length=100)
    TreatedBy = models.CharField(max_length=100)
    BillAmount = models.IntegerField(max_length=100)
    PaidOn  = models.DateField(max_length=100)
    Insurance= models.BooleanField(null=True)
    Patientid = models.ForeignKey(patient, related_name="hospital", on_delete=models.CASCADE)     

    def __str__(self):
        return self.TreatedBy  

    class Meta:
        db_table = "hospitaldb"    
    
