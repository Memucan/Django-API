from rest_framework import serializers
from .models import *

class emptenant(serializers.ModelSerializer):
    class Meta:
        model  = employee
        fields = '__all__'
        
class leavesl(serializers.ModelSerializer):
    class Meta:
        model  = leave
        fields = '__all__'        