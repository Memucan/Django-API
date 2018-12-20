from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from django.db.models import Q

#PatientViews

#Create Method(POST)
class patient1(APIView):
    def post(self,request):

        serializer = Patientsl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Patient Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Read Method(GET)
class patient2(APIView):
    def get(self,request):

        task = patient.objects.all()
        serializer = Patientsl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Update Method(PUT)
class patient3(APIView):
    def put(self, request, pk):
        try:
            task = patient.objects.get(pk=pk)
        except student.DoesNotExist:
            return Response({"Error":"patient Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer =   Patientsl(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"patient details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class patient4(APIView):     
    def delete(self,request, pk):
        try:
            task = patient.objects.get(pk=pk)    
        except patient.DoesNotExist:
            return Response({"Error":"Patient Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)         


#Hospital Record:

#POST 
class hospital1(APIView):
     def post(self, request):

        serializer = hospitalsl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Hospital Record Updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Hospital Records GET
class hospital2(APIView):
    def get(self,request):

        task = hospital.objects.all()
        serializer = hospitalsl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#HospitalUpdate Method(PUT)
class hospital3(APIView):
    def put(self, request, pk):
        try:
            task = hospital.objects.all()
            task = patient.objects.get(pk=pk)
        except student.DoesNotExist:
            return Response({"Error":"patient Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer =   hospitalsl(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"patient details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



#Delete Method
class hospital4(APIView):     
    def delete(self,request, pk):
        try:
            task = hospital.objects.get(pk=pk)    
        except patient.DoesNotExist:
            return Response({"Error":"Patient Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)         

class fullrecord(APIView):
    def get(self, request, pk):
        try:
            task = patient.objects.get(pk=pk)
        except patient.DoesNotExist:
            return Response({"Error":"ID not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = recordsl(task)
        return Response(serializer.data, status=status.HTTP_200_OK) 


#Patient ID and Hospital details
class filter1(APIView):
    def get(self, request):

        value = 13

        task = hospital.objects.filter(id=value)
        serializer = hospitalsl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

#Hospital ID and patient details
class filter2(APIView): 
    def get(self, request):

        value = 15
        
        task = hospital.objects.get(pk=value)
        Patientid = int(task.Patientid_id)
        print(Patientid)

        task2 = patient.objects.get(pk=Patientid)
        serializer = Patientsl(task2)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Patient Treated by Dr.Nandhu or Dr.Meera
class filter3(APIView):
    def get(self,request):

        
        task =  hospital.objects.filter(Q(TreatedBy= "Dr.Meera") | Q(TreatedBy="Dr.Nandhu") )
        serializer = hospitalsl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#patient born from 1990 to 2000
class filter4(APIView):
    def get(self, request):

        task = patient.objects.filter(DOB__range=["2000-01-01", "2010-12-31"])
        serializer = Patientsl(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)         

           

