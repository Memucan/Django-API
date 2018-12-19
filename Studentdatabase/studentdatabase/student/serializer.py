from rest_framework import serializers
from .models import *

class studentsz(serializers.ModelSerializer):

    class Meta:
        model = student
        fields = "__all__"

class studentfeesz(serializers.ModelSerializer):

    class Meta:
        model  = fees
        fields = ('id', 'amount', 'date', 'studentid', 'paidfees')

class stufees(serializers.ModelSerializer):

    fees =  studentfeesz(many = True)  
    class Meta:
        model = student
        fields = '__all__'     
