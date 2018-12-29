from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import *
from.serializer import *

#Create Operation
class movie_create(APIView):
    def post(self,request):

        serializer = moviesl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"movie Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class movie_read(APIView):
    def get(self,request):

        task = movie.objects.all()
        serializer = moviesl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class movie_update(APIView):
    def put(self, request, pk):
        try:
            task = movie.objects.get(pk=pk)
        except movie.DoesNotExist:
            return Response({"Error":"movie Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = moviesl(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"movie details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#Delete Method
class movie_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = movie.objects.get(pk=pk)    
        except movie.DoesNotExist:
            return Response({"Error":"movie Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)   

#------------------------------------------------------------------------------------------------------------------------#

#Cast Details:

#Create Operation
class cast_create(APIView):
    def post(self,request):

        serializer = castsz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"movie Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class cast_read(APIView):
    def get(self,request):

        task = cast.objects.all()
        serializer = castsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class cast_update(APIView):
    def put(self, request, pk):
        try:
            task = cast.objects.get(pk=pk)
        except cast.DoesNotExist:
            return Response({"Error":"movie Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = castsz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"cast details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#Delete Method
class cast_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = cast.objects.get(pk=pk)    
        except cast.DoesNotExist:
            return Response({"Error":"movie Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)   

#fullview
class moviecast(APIView):
    def get(self, request, pk):
        try:
            task = movie.objects.get(pk=pk)
        except movie.DoesNotExist:
            return Response({"Error":"ID not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = moviecastsl(task)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class post_moviecast(APIView):
    def post(self, request, *args, **kwargs):

        serializer = post_moviecastsl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Data Insert successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                           