from django.db import models

class student(models.Model):
    firstname     = models.CharField(max_length=100)
    lastname      = models.CharField(max_length=100)
    dob           = models.DateField()  
    sex           = models.CharField(max_length=10) 
    phone         = models.IntegerField()
    address       = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname

    class Meta:
        db_table = "student_table"       

 
class parents(models.Model):
    fathersname   = models.CharField(max_length=100)
    fathers_occupation  = models.CharField(max_length=100) 
    mothersname   = models.CharField(max_length=100)
    mothers_occupation  = models.CharField(max_length=100)  

    def __str__(self):
        return self.fathersname

    class Meta:
        db_table = "parents_table"       