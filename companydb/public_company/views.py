from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *

#Create Operation
class company_create(APIView):  
    def post(self,request):

        serializer = companysz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"company Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class company_read(APIView):
    def get(self,request):

        task = company.objects.all()
        serializer = companysz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Update Method(PUT)
class company_update(APIView):
    def put(self, request, pk):
        try:
            task = company.objects.get(pk=pk)
        except company.DoesNotExist:
            return Response({"Error":"company Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = companysz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"company details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class company_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = company.objects.get(pk=pk)    
        except company.DoesNotExist:
            return Response({"Error":"company Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)           
