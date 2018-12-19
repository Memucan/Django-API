from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from django.db.models import Q


class studentpost(APIView):
    def post(self,request):

        serializer = studentsz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Student Details Inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class studentget(APIView):
    def get(self,request):

        task = student.objects.all()
        serializer = studentsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class studentdelete(APIView):     
    def delete(self,request, pk):
        try:
            task = student.objects.get(pk=pk)    
        except student.DoesNotExist:
            return Response({"Error":"student Not Found in th Database"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"Message":"Deleted"}, status=status.HTTP_200_OK)       

class studentupdate(APIView):
    def put(self, request, pk):
        try:
            task = student.objects.get(pk=pk)
        except student.DoesNotExist:
            return Response({"Error":"Student Not Found"}, status=status.HTTP_404_NOT_FOUND)   
        serializer =   studentsz(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Student details Updated"}, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class feepost(APIView):
     def post(self, request):

        serializer = studentfeesz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Student Fees Updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class feesget(APIView):
    def get(self,request):

        task = fees.objects.all()
        serializer = studentfeesz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class studentandfees(APIView):
    def get(self, request, pk):
        try:
            task = student.objects.get(pk=pk)
        except student.DoesNotExist:
            return Response({"Error":"ID not Found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = stufees(task)
        return Response(serializer.data, status=status.HTTP_200_OK) 

#FILTERS
 
#NameFilter
class studentfilter(APIView):
    def get(self, request):

        value = "Aravind"         

        task = student.objects.filter(studentname=value)
        serializer = studentsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

#Student ID and Fee details
class studentFilter1(APIView):
    def get(self, request):

        value = 2

        task = fees.objects.filter(studentid_id=value)
        serializer = studentfeesz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#FeesID and Student Details
class studentfilter3(APIView): 
    def get(self, request):

        value = 6
        
        task = fees.objects.get(pk=value)
        studentid = int(task.studentid_id)
        print(studentid)

        task2 = student.objects.get(pk=studentid)
        serializer = studentsz(task2)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Student City and class
class studentfilter2(APIView):
    def get(self,request):

         Value1 = "madurai"
         Value2 = 9

         task = student.objects.filter(City=Value1, standard=Value2)
         serializer = studentsz(task, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

#Rank witthin 5
class studentfilter4(APIView):
    def get(self, request):

        task = student.objects.filter(Rank__lte=5)
        serializer = studentsz(task, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)

#Fees payment Year
class studentfilter5(APIView):
    def get(self, request):

        task = fees.objects.filter(date__range=["2010-01-01", "2017-12-31"])
        serializer = studentfeesz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     

#student Not from Chennai
class studentFilter6(APIView):
    def get(self,request):

        value = 2
        task =  student.objects.filter(~Q(City= "Chennai"), Rank=value )
        serializer = studentsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#student from chennai or rank 3
class studentfilter7(APIView):
    def get(self,request):

        value=2
        task =  student.objects.filter(~Q(City= "Chennai") | Q(Rank=value) )
        serializer = studentsz(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



       