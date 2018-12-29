from rest_framework import serializers
from .models import *

class industrynamesl(serializers.ModelSerializer):
    class Meta:
        model  = industryname
        fields = '__all__'
        