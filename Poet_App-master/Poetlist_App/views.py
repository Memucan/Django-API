from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.core import serializers
from . import config
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Sum



from django.db.models import Q
import os
import boto3
from botocore.client import Config
import datetime
from datetime import timedelta
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create Poet
class view_createpoet(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_all(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)
            local_path =os.path.join(BASE_DIR, "media/")
            image = record.poetimage.name
            local_image_name = str(image)
            full_path_to_file =os.path.join(local_path, local_image_name) 
            print(full_path_to_file)
            remake = str(record.id)
            updatefile = str.replace(local_image_name, local_image_name, remake)
            imagename1 = "PoetImage_" + str(updatefile) +".jpg"
           # try:
            client.upload_file(full_path_to_file,  # Path to local file
                                config.aws_bucket_name,  # Name of Space
                                imagename1)  # Name for remote file
            client.put_object_acl( ACL='public-read', Bucket=config.aws_bucket_name, Key=imagename1 ) 
            os.remove(os.path.join(local_path, image))
            record.poetimage = imagename1
            record.poetimageurl = 'https://s3.amazonaws.com/poetapp/' + imagename1
            record.likes = 0
            record.comments = 0
            record.share = 0
            record.views = 0
            record.save()
            return Response({"Message":"Poet Post Successfully"}, status=status.HTTP_201_CREATED)
            #except:
                # record.likes = 0
                # record.comments = 0
                # record.share = 0
                # record.views = 0
                # record.save()
                # return Response({"Message":"Poet Post Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Poet
class view_updatepoet(APIView):
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_all(task, data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)

            local_path =os.path.join(BASE_DIR, "media/")
            image = record.poetimage.name
            local_image_name = str(image)
            full_path_to_file =os.path.join(local_path, local_image_name) 
            print(full_path_to_file)
            remake = str(record.id)
            updatefile = str.replace(local_image_name, local_image_name, remake)
            imagename1 = "PoetImage_" + str(updatefile) +".jpg"
            try:
                client.upload_file(full_path_to_file,  # Path to local file
                                    config.aws_bucket_name,  # Name of Space
                                    imagename1)  # Name for remote file
                client.put_object_acl( ACL='public-read', Bucket=config.aws_bucket_name, Key=imagename1 ) 
                os.remove(os.path.join(local_path, image))
                record.poetimage = imagename1
                record.poetimageurl = 'https://s3.amazonaws.com/poetapp/' + imagename1
                record.save()
                return Response({"Message":"Poet Update Successfully"}, status=status.HTTP_201_CREATED)
            except:
                return Response({"Message":"Poet Update Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# First Sum View Poet
class view_sumpoet(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_PoetDetails.objects.filter(poststatus='Active').order_by('-createdate')[:20]
        serializer = Sl_Poet_Homeview(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# secound Sum View Poet
class view_sumpoetsec(APIView):
    def get(self, request, *args, **kwargs):
        
        get_data = request.query_params
        skipid = int(get_data['skip'])
        limit = skipid + skipid
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_PoetDetails.objects.filter(poststatus='Active').order_by('-createdate')[skipid:limit]
        serializer = Sl_Poet_Homeview(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Tending Sum View Poet
class view_tensumpoet(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_PoetDetails.objects.filter(posttype='Competition', poststatus='Active').order_by('-createdate')[:20]
        serializer = Sl_Poet_Homeview(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# secound Tending Sum View Poet
class view_tensumpoetsec(APIView):
    def get(self, request, *args, **kwargs):
        
        get_data = request.query_params
        skipid = int(get_data['skip'])
        limit = skipid + skipid
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_PoetDetails.objects.filter(posttype='Competiton', poststatus='Active').order_by('-createdate')[skipid:limit]
        serializer = Sl_Poet_Homeview(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Det View Poet
class view_detailpoet(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)


        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_detview(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Public Poet View
class view_publicptview(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            task.views = int(task.views) + 1
            task.save()
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_detview(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Like for Poet View
class view_poetlikes(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            task.likes = int(task.likes) + 1
            task.save()
            return Response({"Message":"Like Successfully"},status=status.HTTP_200_OK)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

# Share Poet
class view_poetshare(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            task.share = int(task.share) + 1
            task.save()
            return Response({"Message":"Share Successfully"},status=status.HTTP_200_OK)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete Poet
class view_deletepoet(APIView):
    def delete(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)


        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            image1 = task.poetimage.name
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)
        

            client.delete_object(Bucket=config.aws_bucket_name, Key=image1)  # Name for remote file
            task.delete()
            return Response({"Message":"Account Deleted"},status=status.HTTP_200_OK)
        except:
            task.delete()
            return Response({"Message":"Account Deleted"},status=status.HTTP_200_OK)

# Create Poet Comments
class view_createpoetcomments(APIView):
    def post(self, request, *args, **kwargs):

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_PoetCommentsall(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            pk = str(record.postid_id)
            print(pk)
            task = tbl_PoetDetails.objects.get(pk=pk)
            task.comments = int(task.comments) + 1
            task.save()
            return Response({"Message":"Comment Post Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Complaint Poet
class view_createpoetcomplain(APIView):
    def post(self, request, *args, **kwargs):

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_complaint(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Post Complaint Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get Competition
class view_getcomp(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_CompetitionDetails.objects.filter(~Q(name='Defualt', title='Public'), Q(status='Ongoing'))
        serializer = Sl_Poet_getcompetition(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Content & Result
class view_paidsumwinner(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_WinnerDetails.objects.all().order_by('-id')
        serializer = Sl_Poet_winnerall(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Reward History
class view_paidsumpayment(APIView):
    def get(self, request, *args, **kwargs):
        
        filtertype = request.META.get('HTTP_FILTER', None)
        
        today = datetime.date.today()
        if filtertype == "ThisWeek":
            start_week = today - datetime.timedelta(today.weekday())
            end_week = start_week + datetime.timedelta(7)
            task = tbl_PaymentDetails.objects.filter(createdate__range=[start_week, end_week]).order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif filtertype == "All":
            task = tbl_PaymentDetails.objects.all().order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif filtertype == "LastWeek":
            some_day_last_week = timezone.now().date() - timedelta(days=7)
            monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
            monday_of_this_week = monday_of_last_week + timedelta(days=7)
            task = tbl_PaymentDetails.objects.filter(createdate__gte=monday_of_last_week, createdate__lt=monday_of_this_week).order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif filtertype == "ThisMonth":
            current_month = today.month
            task = tbl_PaymentDetails.objects.filter(createdate__month=current_month).order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif filtertype == "Firstprize":
            task = tbl_PaymentDetails.objects.filter(prize="First Prize").order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif filtertype == "Secondprize":
            task = tbl_PaymentDetails.objects.filter(prize="Second Prize").order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif filtertype == "Thirdprize":
            task = tbl_PaymentDetails.objects.filter(prize="Third Prize").order_by('-createdate')
            serializer = Sl_Poet_sumviewpayment(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Error":"Invalid Request"}, status=status.HTTP_404_NOT_FOUND)



# Get User Reward History
class view_getrewardhisuser(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_PaymentDetails.objects.filter(userid_id=pk).order_by('-id')
        serializer = Sl_Poet_sumviewpayment(task, many=True)
        
        totalreward = tbl_PaymentDetails.objects.aggregate(Sum('rewardamount'))
        return Response({ "RewardHistory": serializer.data, "TotalRewardAmount": totalreward }, status=status.HTTP_200_OK)


# Create Notification
class view_createnotifi(APIView):
    def post(self, request, *args, **kwargs):

        serializer = Sl_Poet_notification(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Notification Create Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Notification
class view_updateotifi(APIView):
    def put(self, request, pk, *args, **kwargs):

        try:
            task = tbl_Notification.objects.get(pk=pk)
        except tbl_Notification.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_notification(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Notification Update Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View Notification
class view_sumviewotifi(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        pickup_records=[]
        task = tbl_Notification.objects.filter().order_by('-createdate')
        print(task)
        for each in task:
            notitype = each.notificationtype
            if notitype == "Public":
                record ={"id": each.id, "notificationtitle":each.notificationtitle, "notificationdesc":each.notificationdesc, "notificationtype":each.notificationtype, "assignto":each.assignto, "status":each.status, "createdate":each.createdate }
                pickup_records.append(record)
            elif notitype == "NotPublic":
                if each.assignto == pk:
                    record ={"id": each.id, "notificationtitle":each.notificationtitle, "notificationdesc":each.notificationdesc, "notificationtype":each.notificationtype, "assignto":each.assignto, "status":each.status, "createdate":each.createdate }
                    pickup_records.append(record)
                else:
                    pass
        return Response(pickup_records, status=status.HTTP_200_OK)

# Det View Notification
class view_detailotifi(APIView):
    def get(self, request, pk, *args, **kwargs):

        try:
            task = tbl_Notification.objects.get(pk=pk)
        except tbl_Notification.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_notification(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Delete Notification
class view_deleteotifi(APIView):
    def delete(self, request, pk, *args, **kwargs):

        try:
            task = tbl_Notification.objects.get(pk=pk)
        except tbl_Notification.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)
    
        task.delete()
        return Response({"Message":"Winner list Deleted"},status=status.HTTP_200_OK)
    