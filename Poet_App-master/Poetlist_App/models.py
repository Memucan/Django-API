from django.db import models
import uuid

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

# Poet Comments Table
class tbl_PoetComments(models.Model):
    userid = models.ForeignKey(tbl_Accountholders, models.SET_NULL, null=True)
    postid = models.ForeignKey(tbl_PoetDetails, related_name='Comments', on_delete=models.CASCADE)
    username = models.CharField(null=True, max_length = 100)
    postcomments = models.CharField(null=True, max_length = 500)
    createdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True, max_length = 100)

    def __str__(self):
      return self.username

    class Meta:
        db_table = "tbl_poetcomments"

# Poet Complain Table
class tbl_ComplaintDetails(models.Model):
    compuserid = models.ForeignKey(tbl_Accountholders, models.SET_NULL, null=True)
    postid = models.ForeignKey(tbl_PoetDetails, models.SET_NULL, null=True)
    postuserid = models.CharField(null=True, max_length = 100)
    complainby = models.CharField(null=True, max_length = 100)
    postownername = models.CharField(null=True, max_length = 100)
    posttitle = models.CharField(null=True, max_length = 100)
    complaindesc = models.CharField(null=True, max_length = 500)
    createdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True, max_length = 100)

    def __str__(self):
      return self.posttitle

    class Meta:
        db_table = "tbl_complaintdetails"

# Winner List Table
class tbl_WinnerDetails(models.Model):
    userid = models.ForeignKey(tbl_Accountholders, on_delete=models.CASCADE)
    comptid = models.ForeignKey(tbl_CompetitionDetails, models.SET_NULL, null=True)
    postid = models.ForeignKey(tbl_PoetDetails, models.SET_NULL, null=True)
    comptname = models.CharField(max_length = 100)
    compttitle = models.CharField(null=True, max_length = 100)
    comptdesc = models.CharField(null=True, max_length = 500)
    posttile = models.CharField(max_length = 100)
    postdesc = models.CharField(null=True, max_length = 500)
    postimageurl = models.CharField(null=True, max_length = 200)
    winnername = models.CharField(max_length = 100)
    prizenumber = models.CharField(null=True, max_length = 100)
    likes = models.CharField(null=True, max_length = 100)
    views = models.CharField(null=True, max_length = 100)
    comments = models.CharField(null=True, max_length = 100)
    share = models.CharField(null=True, max_length = 100)
    postdate = models.CharField(null=True, max_length = 100)
    rewarddate = models.CharField(null=True, max_length = 100)
    rewardamount = models.IntegerField(null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True, max_length = 100)

    def __str__(self):
      return self.winnername

    class Meta:
        db_table = "tbl_winnertdetails"

# Payment Table 
class tbl_PaymentDetails(models.Model):
    userid = models.ForeignKey(tbl_Accountholders, models.SET_NULL, null=True)
    comptid = models.ForeignKey(tbl_ComplaintDetails, models.SET_NULL, null=True)
    postid = models.ForeignKey(tbl_PoetDetails, models.SET_NULL, null=True)
    comptname = models.CharField(max_length = 100)
    compttitle = models.CharField(null=True, max_length = 100)
    posttile = models.CharField(max_length = 100)
    postimageurl = models.CharField(null=True, max_length = 200)
    winnername = models.CharField(max_length = 100)
    prize = models.CharField(null=True, max_length = 100)
    bacnkname = models.CharField(null=True, max_length = 100)
    acnumber = models.CharField(null=True, max_length = 100)
    ifcscode = models.CharField(null=True, max_length = 100)
    rewardamount = models.IntegerField(null=True)
    refernceid = models.CharField(null=True, max_length = 100)
    createdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True, max_length = 100)

    def __str__(self):
      return self.winnername

    class Meta:
        db_table = "tbl_paymentdetails"

# Notification Table 
class tbl_Notification(models.Model):
    notificationtitle = models.CharField(max_length = 100)
    notificationdesc = models.CharField(null=True, max_length = 500)
    notificationtype = models.CharField(null=True, max_length = 200)
    assignto = models.CharField(null=True, max_length = 100)
    status = models.CharField(null=True, max_length = 100)
    createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.notificationtitle

    class Meta:
        db_table = "tbl_notification"