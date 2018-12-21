from rest_framework import serializers
from .models import *

class serial_music(serializers.ModelSerializer):

    class Meta:
        model = music 
        fields = '__all__'