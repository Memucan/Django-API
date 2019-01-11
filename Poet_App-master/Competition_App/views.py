from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.core import serializers
 
# 
# Sum View for On Going Competition
class view_sumcompongng(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_CompetitionDetails.objects.filter(status='Ongoing')
        serializer = Sl_Comp_SumView(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
