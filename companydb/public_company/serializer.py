from rest_framework import serializers
from .models import *

class companysz(serializers.ModelSerializer):
    class Meta:
        model  = company
        fields = '__all__'
        