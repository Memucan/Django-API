from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *

#School Create Operation
class school_create(APIView):  
    def post(self,request):

        serializer = schoolsz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"school Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class school_read(APIView):
    def get(self,request):

        task = school.objects.all()
        serializer = schoolsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Update Method(PUT)
class school_update(APIView):
    def put(self, request, pk):
        try:
            task = school.objects.get(pk=pk)
        except school.DoesNotExist:
            return Response({"Error":"school Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = schoolsz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"school details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class school_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = school.objects.get(pk=pk)    
        except school.DoesNotExist:
            return Response({"Error":"school Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)           
