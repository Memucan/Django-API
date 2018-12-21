from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *

class postvideo(APIView):
    def post(self, request, ):

        serializer = s_video(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Video Uploaded Successfully"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class getvideo(APIView):
    def get(self, request):

       task = video.objects.all()
       serializer = s_video(task, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)

class getspecificmusic(APIView):
    def get(self, request, pk) :
        try:
            task = video.objects.get(pk=pk)
        except video.DoesNotExist:
            return Response({"Error":"Video not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = s_video(task)  
        return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)  

class deletevideo(APIView):
    def delete(self, request, pk):
        try:
            task = video.objects.get(pk=pk)
        except video.DoesNotExist:
            return Response({"Error":"video not found"}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_202_ACCEPTED)

