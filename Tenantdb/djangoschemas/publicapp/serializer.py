from rest_framework import serializers
from .models import *

class schoolsz(serializers.ModelSerializer):
    class Meta:
        model  = school
        fields = '__all__'
        