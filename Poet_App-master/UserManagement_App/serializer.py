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
        fields = ('id', 'userimageurl', 'firstname', 'lastname', 'emailid')  

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

