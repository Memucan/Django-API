from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *

#Create Operation
class industryname_create(APIView):  
    def post(self,request):

        serializer = industrynamesl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"industryname Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class industryname_read(APIView):
    def get(self,request):

        task = industryname.objects.all()
        serializer = industrynamesl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Update Method(PUT)
class industryname_update(APIView):
    def put(self, request, pk):
        try:
            task = industryname.objects.get(pk=pk)
        except industryname.DoesNotExist:
            return Response({"Error":"industryname Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = industrynamesl(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"industryname details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class industryname_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = industryname.objects.get(pk=pk)    
        except industryname.DoesNotExist:
            return Response({"Error":"industryname Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)           
