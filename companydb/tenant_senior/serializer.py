from rest_framework import serializers
from .models import *

#SeniorSerializer
class seniorsz(serializers.ModelSerializer):
    class Meta:
        model = senior
        fields = "__all__"

#qualificationSerializer
class qualificationsz(serializers.ModelSerializer):
    class Meta:
        model = qualification
        fields = "__all__" 

class seniorandqual(serializers.ModelSerializer):

    qualification = qualificationsz(many = True)  
    class Meta:
        model = senior
        fields = '__all__'             