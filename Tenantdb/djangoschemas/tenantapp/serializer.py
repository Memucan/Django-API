from rest_framework import serializers
from .models import *

class tenantsz(serializers.ModelSerializer):
    class Meta:
        model  = student
        fields = '__all__'
        