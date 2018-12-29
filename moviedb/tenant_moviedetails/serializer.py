from rest_framework import serializers
from .models import *

class moviesl(serializers.ModelSerializer):
    class Meta:
        model  = movie
        fields = '__all__'
        
#castSerializer
class castsz(serializers.ModelSerializer):
    class Meta:
        model = cast
        fields = "__all__" 

#get movie and cast in same tab
class moviecastsl(serializers.ModelSerializer):

    cast = castsz(many = True)  
    class Meta:
        model = movie
        fields = '__all__'             

class movieandcast_postsl(serializers.ModelSerializer):

    class Meta:
        model = cast
        fields = ('hero', 'heroine', 'villain', 'movieid_id')



#post senior and qulification in same tab       

class post_moviecastsl(serializers.ModelSerializer):

    cast= movieandcast_postsl(many=True)

    class Meta:
        model = movie
        fields = '__all__'
        
    def create(self, validated_data):
        moviedata = validated_data.pop('cast')              
        moviedata2 = movie.objects.create(**validated_data)
        print(moviedata2)
        for obtaineddata in moviedata:    
            print(moviedata2.id)      
            cast.objects.create(movieid_id=moviedata2.id ,**obtaineddata)
        return moviedata2