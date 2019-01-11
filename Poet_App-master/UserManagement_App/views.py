from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from . import config
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.core import serializers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens1 import account_activation_token1
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Sum

import os
import boto3
from botocore.client import Config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Login Mobile User
class Vw_User_Login(APIView):
    def get(self, request):
        get_data = request.query_params

        try:
            User = tbl_Accountholders.objects.get(username=get_data['username'], password=get_data['password'])
            if User.accountstatus == 'Active':
                serializer = Sl_User_Login_check(User)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Error":"Account is In-Active, Please contact us"}, status=status.HTTP_201_CREATED)

        except tbl_Accountholders.DoesNotExist:
            raise exceptions.AuthenticationFailed('Username or Password is invalid. Please re-enter the appropriate credentials')

# Social Login Mobile User
class Vw_User_SoicalLogin(APIView):
    def get(self, request):
        get_data = request.query_params

        try:
            User = tbl_Accountholders.objects.get(socialtype=get_data['socialtype'], socialtypetoken=get_data['socialtypetoken'])
            if User.accountstatus == 'Active':
                serializer = Sl_User_Login_check(User)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Error":"Account is In-Active, Please contact us"}, status=status.HTTP_201_CREATED)

        except tbl_Accountholders.DoesNotExist:
            raise exceptions.AuthenticationFailed('Social Media Login Failed ')
                 

# Forgot Password
class Vw_User_ForgotPassword(APIView):
        def get(self, request):
            get_data = request.query_params
            try: 
                user = tbl_Accountholders.objects.get(username=get_data['username'], emailid=get_data['emailid'])       
                email = get_data['emailid']
                firstname = user.firstname
                lastname = user.lastname
                Userid = user.id
                message = render_to_string('forgot_Password.html', {
                    'lastname': lastname,
                    'firstname': firstname,
                    'userid': Userid,
                    'uid': urlsafe_base64_encode(force_bytes(Userid)).decode(),
                    'token': account_activation_token1.make_token(Userid),
                })
                mail_subject = 'Poet App Forgot Password Link'
                to_email = email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return Response({"Message":"Reset Password link has been sent to your register Email-ID"}, status=status.HTTP_201_CREATED)         
            except tbl_Accountholders.DoesNotExist:
                raise exceptions.AuthenticationFailed('Username, Email id is invalid. Please re-enter the appropriate credentialls')
         
# Password Reset
class reset_Password(APIView):      
    def get(self, request):
        try:
            get_data = request.query_params
            uid = force_text(urlsafe_base64_decode(get_data['authkey']))
            token = get_data['token']
            user = tbl_Accountholders.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, tbl_Accountholders.DoesNotExist):
            user = None
        if user is not None and account_activation_token1.check_token(uid, token):

            tbl_Accountholders.objects.filter(id=uid).update(password=get_data['password'])
            return Response({"Message":"Password Reset Sucessfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Activation link is invalid!"}, status=status.HTTP_404_NOT_FOUND)


# Account Register
class view_createacc(APIView):
    parser_classes = (MultiPartParser, FormParser) 
    def post(self, request, *args, **kwargs):

        serializer = Sl_User_Register(data=request.data)
        if serializer.is_valid():
            record = serializer.save()

            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)

            local_path =os.path.join(BASE_DIR, "media/")
            image = record.userimage.name
            local_image_name = str(image)
            full_path_to_file =os.path.join(local_path, local_image_name) 
            print(full_path_to_file)
            remake = str(record.id)
            updatefile = str.replace(local_image_name, local_image_name, remake)
            imagename1 = "AccountProfileImage_" + str(updatefile) +".jpg"
            try:
                client.upload_file(full_path_to_file,  # Path to local file
                                    config.aws_bucket_name,  # Name of Space
                                    imagename1)  # Name for remote file
                client.put_object_acl( ACL='public-read', Bucket=config.aws_bucket_name, Key=imagename1 ) 
                os.remove(os.path.join(local_path, image))
                record.accountimage = imagename1
                record.accountimageurl = 'https://s3.amazonaws.com/poetappbucket/' + imagename1
                record.save()
                return Response({"Message":"User Registered Successfully"}, status=status.HTTP_201_CREATED)
            except:
            # conn = S3Connection('AKIAJQCLNDGHCOMVFNAA', 'YPJ5SZJjmARhaPhP0wa0tCHT2OUIwvGXtqjdoUgZ')
            # bucket = conn.get_bucket(config.aws_bucket_name)
            # k = Key(bucket)
            # k.key = 'imagename1.jpg'# for example, 'images/bob/resized_image1.png'
            # k.set_contents_from_file(full_path_to_file)
                return Response({"Message":"User Registered Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Account
class view_updateacc(APIView):
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_Accountholders.objects.get(pk=pk)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_User_Register(task, data=request.data)
        if serializer.is_valid():
            record = serializer.save()

            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)

            local_path =os.path.join(BASE_DIR, "media/")
            image = record.userimage.name
            local_image_name = str(image)
            full_path_to_file =os.path.join(local_path, local_image_name) 
            print(full_path_to_file)
            remake = str(record.id)
            updatefile = str.replace(local_image_name, local_image_name, remake)
            imagename1 = "AccountProfileImage_" + str(updatefile) +".jpg"
            try:
                client.upload_file(full_path_to_file,  # Path to local file
                                    config.aws_bucket_name,  # Name of Space
                                    imagename1)  # Name for remote file
                client.put_object_acl( ACL='public-read', Bucket=config.aws_bucket_name, Key=imagename1 ) 
                os.remove(os.path.join(local_path, image))
                record.accountimage = imagename1
                record.accountimageurl = 'https://s3.amazonaws.com/poetappbucket/' + imagename1
                record.save()
                return Response({"Message":"User Update Successfully"}, status=status.HTTP_201_CREATED)
            except:
            # conn = S3Connection('AKIAJQCLNDGHCOMVFNAA', 'YPJ5SZJjmARhaPhP0wa0tCHT2OUIwvGXtqjdoUgZ')
            # bucket = conn.get_bucket(config.aws_bucket_name)
            # k = Key(bucket)
            # k.key = 'imagename1.jpg'# for example, 'images/bob/resized_image1.png'
            # k.set_contents_from_file(full_path_to_file)
                return Response({"Message":"User Update Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Det View Account
class view_detailacc(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)


        try:
            task = tbl_Accountholders.objects.get(pk=pk)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_User_Register(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Profile View with post 
class view_profpost(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_Accountholders.objects.get(pk=pk)
            serializer = Sl_User_SumView(task)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Poet is not found"}, status=status.HTTP_404_NOT_FOUND)

        postcount = tbl_PoetDetails.objects.filter(userid=pk).count() 
        totallikes = tbl_PoetDetails.objects.filter(userid=pk).aggregate(Sum('likes'))
        post = tbl_PoetDetails.objects.filter(userid=pk).order_by('id')
        serializer1 = Sl_Poet_all(post, many=True)

        return Response({ "profile": serializer.data, "Post": serializer1.data, "TotalPost": postcount, "TotallLikes": totallikes}, status=status.HTTP_200_OK)

# get Image for poet
class view_getimagepoet(APIView):
    def get(self, request, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Accountholders.objects.get(securitycode=code)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_ImageTemplates.objects.filter(status='True')
        serializer = Sl_Poet_image(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


