from rest_framework import serializers
from .models import *

class s_video(serializers.ModelSerializer):
  
    class Meta:
        model = video
        fields = '__all__'
