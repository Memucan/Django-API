from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
 
class view_music(APIView):
    def post(self, request, pk):
        
        serializer = serial_music(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Data Insert successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class view_music1(APIView):
    def get(self,request):

        task = music.objects.all()
        serializer = serial_music(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class getmusic(APIView):
    def get(self, request, pk):
        try:
            task = music.objects.get(pk=pk)
        except music.DoesNotExist:
            return Response({"Music Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serial_music(task)
        return Response(serializer.data, status=status.HTTP_302_FOUND)  

class updatemusic(APIView):
    def put(self, request, pk):
        try:
            task = music.objects.get(pk=pk) 
        except music.DoesNotExist:
            return Response({"Error":"Music Not Found"}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS) 

        serializer = serial_music(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Music Updated successfully"}, status=status.HTTP_202_ACCEPTED) 
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class deletemusic(APIView):
    def delete(self, request, pk):
        try:
            task = music.objects.get(pk=pk)
        except music.DoesNotExist:
            return Response({"Error": "Song Kedaikala"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message": "Song Deleted"}, status=status.HTTP_502_BAD_GATEWAY)
        
