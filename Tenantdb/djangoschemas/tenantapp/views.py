from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import *
from.serializer import *

#Student Create Operation
class student_create(APIView):
    def post(self,request):

        serializer = tenantsz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Student Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Student Read Operation
class student_read(APIView):
    def get(self,request):

        task = student.objects.all()
        serializer = tenantsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class student_update(APIView):
    def put(self, request, pk):
        try:
            task = student.objects.get(pk=pk)
        except student.DoesNotExist:
            return Response({"Error":"student Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = tenantsz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"student details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class student_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = student.objects.get(pk=pk)    
        except student.DoesNotExist:
            return Response({"Error":"student Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)   