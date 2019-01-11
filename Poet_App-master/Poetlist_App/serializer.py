from rest_framework import serializers
from .models import *



class Sl_Poet_Homeview(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PoetDetails
        fields = ('id', 'poettitle', 'poetimageurl', 'likes', 'share', 'comments', 'views', 'createdate')  

class Sl_Poet_all(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PoetDetails
        fields = '__all__'  


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


class Sl_Poet_complaint(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_ComplaintDetails
        fields = '__all__'  


class Sl_Poet_sumviewcomplaint(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_ComplaintDetails
        fields = ('id', 'posttitle', 'complainby', 'postownername', 'complaindesc', 'createdate', 'postid')


class Sl_Poet_getcompetition(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_CompetitionDetails
        fields = ('id', 'title', 'name')


class Sl_Poet_winnerall(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_WinnerDetails
        fields = '__all__'

class Sl_Poet_sumviewpayment(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_PaymentDetails
        fields = ('id', 'postid', 'comptid', 'userid', 'comptname', 'compttitle', 'winnername', 'prize', 'bacnkname', 'ifcscode', 'rewardamount', 'createdate')

class Sl_Poet_notification(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_Notification
        fields = '__all__'