from django.db import models

class student(models.Model):
    studentname = models.CharField(max_length=100, null=True)
    rollnumber  = models.IntegerField(null=True)
    standard    = models.IntegerField(null=True)
    section     = models.CharField(max_length=100, null=True)
    DOB         = models.DateField(null=True)
    City        = models.CharField(max_length=100, null=True)
    state       = models.CharField(max_length=100, null=True)
    Rank        = models.IntegerField(null=True)
    email       = models.EmailField(null=True)
    phone       = models.IntegerField(null=True)

    def __str__(self):
        return self.studentname

    class Meta:
        db_table = "studentbase"        
    
class fees(models.Model):
    amount = models.IntegerField()
    date = models.DateField()
    paidfees= models.BooleanField(null=True)
    paidby = models.CharField(max_length=100, null=True)
    studentid = models.ForeignKey(student, related_name="fees", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.paidby

    class meta: 
        db_table = "feestable"    
