from django.db import models

class senior(models.Model):
    firstname     = models.CharField(max_length=100)
    lastname      = models.CharField(max_length=100)
    dob           = models.DateField()  
    sex           = models.CharField(max_length=10) 
    phone         = models.IntegerField()
    address       = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname

    class Meta:
        db_table = "senior_table"    

class qualification(models.Model):
    tenthpercentage  = models.IntegerField()
    twelfthpercentage= models.IntegerField()
    ugpercentage     = models.IntegerField()
    pgpercentage     = models.IntegerField()
    seniorid = models.ForeignKey(senior, related_name="qualification", on_delete=models.CASCADE)

    def __str__(self):
        return self.tenthpercentage

    class Meta:
        db_table = "qualification_table"         