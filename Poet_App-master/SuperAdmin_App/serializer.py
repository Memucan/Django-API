from rest_framework import serializers
from .models import *

 

class Sl_User_Login_check(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Accountholders
        fields = ('id', 'userimageurl', 'firstname', 'lastname', 'emailid', 'securitycode')  

class Sl_User_Login_Admincheck(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Adminuser
        fields = ('id', 'userimageurl', 'name', 'role', 'permission', 'securitycode')

class Sl_User_Login_Adminpass(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Adminuser
        fields = ('id', 'password')  

class Sl_User_SumView(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Accountholders
        fields = ('id', 'userimageurl', 'firstname', 'lastname', 'emailid', 'kpaccountname', 'gender', 'dateofbirth', 'accountstatus')  


class Sl_User_ActiveorInactive(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Accountholders
        fields = ('id', 'accountstatus')  


class Sl_User_Register(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Accountholders
        fields = '__all__'  


class Sl_User_updateadmin(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Adminuser
        fields = '__all__'  


class Sl_Poet_all(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PoetDetails
        fields = '__all__'  

class Sl_Poet_image(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_ImageTemplates
        fields = '__all__'  


class Sl_Comp_SumView(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_CompetitionDetails
        fields = ('id', 'title', 'name', 'description', 'startdate', 'enddate', 'finishdate')  

class Sl_Comp_all(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_CompetitionDetails
        fields = '__all__'  


class Sl_Poet_complaint(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_ComplaintDetails
        fields = '__all__'  


class Sl_Poet_sumviewcomplaint(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_ComplaintDetails
        fields = ('id', 'posttitle', 'complainby', 'postownername', 'complaindesc', 'createdate', 'postid')


class Sl_Poet_PoetCommentsall(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PoetComments
        fields = '__all__'  

class Sl_Poet_detview(serializers.ModelSerializer):
    Comments = serializers.SerializerMethodField()
    class Meta:
        model = tbl_PoetDetails
        fields = '__all__'  

    def get_Comments(self, instance):
        datalist = instance.Comments.all().order_by('id')
        return Sl_Poet_PoetCommentsall(datalist, many=True).data


class Sl_Poet_campidetview(serializers.ModelSerializer):
    class Meta:
        model = tbl_PoetDetails
        fields = '__all__'  

class Sl_Poet_competitiondetview(serializers.ModelSerializer):
    Poets = serializers.SerializerMethodField()
    class Meta:
        model = tbl_CompetitionDetails
        fields = '__all__'

    def get_Poets(self, instance):
        datalist = instance.Poets.all().order_by('id')
        return Sl_Poet_campidetview(datalist, many=True).data


class Sl_Poet_sumviewwinnder(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_WinnerDetails
        fields = ('id', 'comptname', 'comptdesc', 'compttitle', 'winnername', 'posttile', 'prizenumber', 'likes', 'views', 'comments')

class Sl_Poet_winnerall(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_WinnerDetails
        fields = '__all__'


class Sl_Poet_sumviewpayment(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PaymentDetails
        fields = ('id', 'comptname', 'compttitle', 'winnername', 'prize', 'bacnkname', 'ifcscode', 'rewardamount', 'createdate')

class Sl_Poet_paymentall(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PaymentDetails
        fields = '__all__'

class Sl_Poet_notification(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Notification
        fields = '__all__'
