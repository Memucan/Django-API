from django.db import models
import uuid


# Competition Table
class tbl_CompetitionDetails(models.Model):
    title = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    description = models.CharField(null=True, max_length = 500)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    finishdate = models.DateTimeField()
    starttime = models.CharField(null=True, max_length = 100)
    endtime = models.CharField(null=True, max_length = 100)
    finishtime = models.CharField(null=True, max_length = 100)
    createdate = models.DateTimeField(auto_now_add=True)
    createby = models.CharField(null=True, max_length = 200)
    status = models.CharField(null=True, max_length = 100)

    def __str__(self):
      return self.title

    class Meta:
        db_table = "tbl_competitiondetails"

# Account Holder
class tbl_Accountholders(models.Model):
    userimage = models.ImageField(blank=True, null=True)
    userimageurl = models.CharField(null=True,max_length = 100)
    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(null=True, max_length = 200)
    emailid = models.CharField(max_length = 150)
    gender = models.CharField(max_length = 100)
    dateofbirth = models.CharField(max_length = 100)
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    phonenumber = models.CharField(null=True, max_length = 200)
    kpaccountname = models.CharField(max_length = 200)
    bankname = models.CharField(null=True, max_length = 200)
    ifcscode = models.CharField(null=True, max_length = 100)
    accountstatus = models.CharField(null=True, max_length = 100)
    createdate = models.DateTimeField(auto_now_add=True)
    role = models.CharField(null=True, max_length = 100)
    socialtype = models.CharField(null=True, max_length = 200)
    socialtypetoken = models.CharField(null=True, max_length = 200)
    securitycode = models.CharField(null=True, max_length=100, blank=True, default=uuid.uuid4)


    def __str__(self):
      return self.firstname

    class Meta:
        db_table = "tbl_Accountholders"

# Poet Table
class tbl_PoetDetails(models.Model):
    userid = models.ForeignKey(tbl_Accountholders, on_delete=models.CASCADE)
    conpetitionid = models.ForeignKey(tbl_CompetitionDetails, on_delete=models.CASCADE)
    username = models.CharField(null=True, max_length = 100)
    competitionname = models.CharField(max_length = 100)
    poettitle = models.CharField(max_length = 100)
    poetimage = models.ImageField(blank=True, null=True)
    poetimageurl = models.CharField(null=True, max_length = 200)
    description = models.CharField(null=True, max_length = 200)
    likes = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)
    share = models.IntegerField(null=True)
    views = models.IntegerField(null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    posttype = models.CharField(null=True, max_length = 100)
    poststatus = models.CharField(null=True, max_length = 100)

    def __str__(self):
      return self.poettitle

    class Meta:
        db_table = "tbl_poetdetails"
