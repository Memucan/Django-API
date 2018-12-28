from django.db import models

class employee(models.Model):
    firstname     = models.CharField(max_length=100)
    lastname      = models.CharField(max_length=100)
    dob           = models.DateField()  
    sex           = models.CharField(max_length=10) 
    phone         = models.IntegerField()
    address       = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname

    class Meta:
        db_table = "employee"    

class leave(models.Model):
    numberofdays  = models.IntegerField(max_length=100)
    fromdate      = models.DateField(max_length=100)
    todate        = models.DateField()  
    reason        = models.CharField(max_length=10) 
 

    def __str__(self):
        return self.numberofdays

    class Meta:
        db_table = "leave_table"          