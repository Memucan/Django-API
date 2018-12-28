from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import *
from.serializer import *

#Create Operation
class employee_create(APIView):
    def post(self,request):

        serializer = emptenant(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"employee Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class employee_read(APIView):
    def get(self,request):

        task = employee.objects.all()
        serializer = emptenant(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class employee_update(APIView):
    def put(self, request, pk):
        try:
            task = employee.objects.get(pk=pk)
        except employee.DoesNotExist:
            return Response({"Error":"employee Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = emptenant(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"employee details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#Delete Method
class employee_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = employee.objects.get(pk=pk)    
        except employee.DoesNotExist:
            return Response({"Error":"employee Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)   

###############################################################################################

#Create Operation
class leave_create(APIView):
    def post(self,request):

        serializer = leavesl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"leave Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Operation
class leave_read(APIView):
    def get(self,request):

        task = leave.objects.all()
        serializer = leavesl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Update Method(PUT)
class leave_update(APIView):
    def put(self, request, pk):
        try:
            task = leave.objects.get(pk=pk)
        except leave.DoesNotExist:
            return Response({"Error":"leave Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer = leavesl(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"leave details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#Delete Method
class leave_delete(APIView):     
    def delete(self,request, pk):
        try:
            task = leave.objects.get(pk=pk)    
        except leave.DoesNotExist:
            return Response({"Error":"leave Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)   

class leave_getuser(APIView):
    def get(self, request, pk):
        try:
            task = leave.objects.get(pk=pk)
        except leave.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = leavesl(task)
        return Response(serializer.data, status=status.HTTP_200_OK)        
        