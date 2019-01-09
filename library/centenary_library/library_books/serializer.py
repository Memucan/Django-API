from rest_framework import serializers
from .models import *

#BOOKSerializer
class books_serializer(serializers.ModelSerializer):
    class Meta:
        model = model_books
        fields = "__all__"

#ChapterSerializer
class chapter_serilaizer(serializers.ModelSerializer):
    class Meta:
        model = model_chapters
        fields = "__all__" 

#books and chapter
class bookndchapter_serializer(serializers.ModelSerializer):
    
    book_chapters = chapter_serilaizer(many=True)
    class Meta:
        model = model_books
        fields ="__all__"    

#PageSerializer
class page_serilaizer(serializers.ModelSerializer):
    class Meta:
        model = model_page
        fields = "__all__" 

#books and chapter
class chapterndpage_serializer(serializers.ModelSerializer):
    
    chapters_page = page_serilaizer(many=True)
    class Meta:
        model = model_chapters
        fields = "__all__"            