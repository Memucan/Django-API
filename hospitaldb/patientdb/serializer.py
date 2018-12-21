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

class hospitaldetailsl(serializers.ModelSerializer):
    
    class Meta:
        model = hospital
        fields = ('Illness', 'TreatedBy', 'BillAmount', 'PaidOn','Insurance','Patientid_id')  
        

class patienthospitalsl(serializers.ModelSerializer):

    hospital = hospitaldetailsl(many=True)

    class Meta:
        model = patient
        fields = '__all__'
        
    def create(self, validated_data):
        newdata = validated_data.pop('hospital')              
        newdata2 = patient.objects.create(**validated_data)
        print(newdata2)
        for obtaineddata in newdata:    
            print(newdata2.id)      
            hospital.objects.create(Patientid_id=newdata2.id ,**obtaineddata)
        return newdata2
