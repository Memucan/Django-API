from rest_framework import serializers
from .models import *



class Sl_Comp_SumView(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_CompetitionDetails
        fields = ('id', 'title', 'name', 'description', 'startdate', 'enddate', 'finishdate')  

class Sl_Comp_all(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_CompetitionDetails
        fields = '__all__'  
