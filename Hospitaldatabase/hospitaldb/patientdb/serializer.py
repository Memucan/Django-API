from rest_framework import serializers
from .models import *

#PatientSerializer
class Patientsl(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = "__all__"

#HospitalSerializer
class hospitalsl(serializers.ModelSerializer):
    class Meta:
        model = hospital
        fields = "__all__" 

#FullRecord

class recordsl(serializers.ModelSerializer):
    
    hospital = hospitalsl(many=True)
    class Meta:
        model = patient
        fields = "__all__"                