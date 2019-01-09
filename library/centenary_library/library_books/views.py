from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from django.db.models import Q

#Create Method(POST)
class post_book(APIView):
    def post(self,request):

        serializer = books_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Book Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Method(GET)
class read_book(APIView):
    def get(self,request):

        task = model_books.objects.all()
        serializer = books_serializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Update Method(PUT)
class update_book(APIView):
    def put(self, request, pk):
        try:
            task = model_books.objects.get(pk=pk)
        except model_books.DoesNotExist:
            return Response({"Error":"Book Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer =   books_serializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Book details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


#Delete Method
class delete_book(APIView):     
    def delete(self,request, pk):
        try:
            task = model_books.objects.get(pk=pk)    
        except model_books.DoesNotExist:
            return Response({"Error":"Book Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)         

########################################################################################################
#POST 
class post_chapter(APIView):
     def post(self, request):

        serializer = chapter_serilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"chapter Updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Chapter GET
class get_chapter(APIView):
    def get(self,request):

        task = model_chapters.objects.all()
        serializer = chapter_serilaizer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Method(PUT)
class put_chapter(APIView):
    def put(self, request, pk):
        try:
            task = model_chapters.objects.get(pk=pk)
        except model_chapters.DoesNotExist:
            return Response({"Error":"Chapters Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer =   chapter_serilaizer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Chapter details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class delete_chapter(APIView):     
    def delete(self,request, pk):
        try:
            task = model_chapters.objects.get(pk=pk)    
        except model_chapters.DoesNotExist:
            return Response({"Error":"chapter Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)         

class bookndchapter_get(APIView):
    def get(self, request, pk):
        try:
            task = model_books.objects.get(pk=pk)
        except model_books.DoesNotExist:
            return Response({"Error":"ID not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = bookndchapter_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK) 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

#POST 
class post_page(APIView):
     def post(self, request):

        serializer = page_serilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Page Updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Chapter GET
class get_page(APIView):
    def get(self,request):

        task = model_page.objects.all()
        serializer = page_serilaizer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Method(PUT)
class put_page(APIView):
    def put(self, request, pk):
        try:
            task = model_page.objects.get(pk=pk)
        except model_page.DoesNotExist:
            return Response({"Error":"Page Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer =   page_serilaizer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Page details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class delete_page(APIView):     
    def delete(self,request, pk):
        try:
            task = model_page.objects.get(pk=pk)    
        except model_page.DoesNotExist:
            return Response({"Error":"Page Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)         

class chapterndpage_get(APIView):
    def get(self, request, pk):
        try:
            task = model_chapters.objects.get(pk=pk)
        except model_chapters.DoesNotExist:
            return Response({"Error":"ID not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = chapterndpage_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK) 