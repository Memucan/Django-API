from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import *
from.serializer import *

#Create Operation
class senior_create(APIView):
    def post(self,request):

        serializer = seniorsz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"employee Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class senior_read(APIView):
    def get(self,request):

        task = senior.objects.all()
        serializer = seniorsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class senior_update(APIView):
    def put(self, request, pk):
        try:
            task = senior.objects.get(pk=pk)
        except senior.DoesNotExist:
            return Response({"Error":"employee Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = seniorsz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"employee details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#Delete Method
class senior_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = senior.objects.get(pk=pk)    
        except senior.DoesNotExist:
            return Response({"Error":"employee Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)  
###############################################################################################

#Create Operation
class qualification_create(APIView):
    def post(self,request):

        serializer = qualificationsz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"qualification Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class qualification_read(APIView):
    def get(self,request):

        task = qualification.objects.all()
        serializer = qualificationsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class qualification_update(APIView):
    def put(self, request, pk):
        try:
            task = qualification.objects.get(pk=pk)
        except qualification.DoesNotExist:
            return Response({"Error":"qualification Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = qualificationsz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"qualification details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#Delete Method
class qualification_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = qualification.objects.get(pk=pk)    
        except qualification.DoesNotExist:
            return Response({"Error":"qualification Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)   

#fullview
class seniorqual(APIView):
    def get(self, request, pk):
        try:
            task = senior.objects.get(pk=pk)
        except senior.DoesNotExist:
            return Response({"Error":"ID not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = seniorandqual(task)
        return Response(serializer.data, status=status.HTTP_200_OK) 