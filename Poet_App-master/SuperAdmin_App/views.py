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
from django.db.models import Q

import os
import boto3
from botocore.client import Config
from boto.s3.connection import S3Connection
from boto3.s3.transfer import S3Transfer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dashboard
class view_dashboard(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        totallacc = tbl_Accountholders.objects.all().count()
        activeacc = tbl_Accountholders.objects.filter(accountstatus='Active').count()
        activeinacc = tbl_Accountholders.objects.filter(accountstatus='In-Active').count()
        totallcom = tbl_CompetitionDetails.objects.all().count()
        activecom = tbl_CompetitionDetails.objects.filter(status='Active').count()
        activeincom = tbl_CompetitionDetails.objects.filter(status='In-Active').count()
        record = {"Total_Account": totallacc, "Active_Account": activeacc, "InActive_Account": activeinacc, 
        "Total_Competition": totallcom, "Active_Competition": activecom, "InActive_Competition": activeincom }
            
        return Response(record, status=status.HTTP_200_OK)

# Login Admin User
class Vw_User_AdminLogin(APIView):
    def get(self, request):
        get_data = request.query_params

        try:
            User = tbl_Adminuser.objects.get(username=get_data['username'], password=get_data['password'], emailid=get_data['emailid'])
            if User.userstatus == 'Active':
                serializer = Sl_User_Login_Admincheck(User)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Error":"Account is In-Active, Please contact us"}, status=status.HTTP_201_CREATED)

        except tbl_Adminuser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Username or Password is invalid. Please re-enter the appropriate credentials')
 
# Forgot Password
class Vw_User_ForgotPassword(APIView):
        def get(self, request):
            get_data = request.query_params
            try: 
                user = tbl_Adminuser.objects.get(username=get_data['username'], emailid=get_data['emailid'])       
                email = get_data['emailid']
                name = user.name
                Userid = user.id
                message = render_to_string('forgot_Password.html', {
                    'firstname': name,
                    'uid': urlsafe_base64_encode(force_bytes(Userid)).decode(),
                    'token': account_activation_token1.make_token(Userid),
                })
                mail_subject = 'Poet App Forgot Password Link'
                to_email = email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return Response({"Message":"Reset Password link has been sent to your register Email-ID"}, status=status.HTTP_201_CREATED)         
            except tbl_Adminuser.DoesNotExist:
                raise exceptions.AuthenticationFailed('Username, Email id is invalid. Please re-enter the appropriate credentialls')
         
# Password Reset
class reset_Password(APIView):      
    def get(self, request):
        try:
            get_data = request.query_params
            uid = force_text(urlsafe_base64_decode(get_data['authkey']))
            token = get_data['token']
            user = tbl_Adminuser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, tbl_Adminuser.DoesNotExist):
            user = None
        if user is not None and account_activation_token1.check_token(uid, token):

            tbl_Adminuser.objects.filter(id=uid).update(password=get_data['password'])
            return Response({"Message":"Password Reset Sucessfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Activation link is invalid!"}, status=status.HTTP_404_NOT_FOUND)



# Admin User password Validating
class Vw_User_Adminpassw(APIView):
    def put(self, request, pk):
        get_data = request.query_params
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            task = tbl_Adminuser.objects.get(securitycode=code, pk=pk, password=get_data['password'])
            return Response({"Message":"Valid Password"}, status=status.HTTP_201_CREATED)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Password"}, status=status.HTTP_404_NOT_FOUND)



# Update Admin User
class view_updateadmin(APIView):
    def put(self, request, pk, *args, **kwargs):
	
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)
			
        try:
            task = tbl_Adminuser.objects.get(pk=pk)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_User_updateadmin(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Admin Updated Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Admin User Password
class view_updatepass(APIView):
    def put(self, request, pk, *args, **kwargs):
        crpassword = request.META.get('HTTP_PASSWORD', None)
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            task = tbl_Adminuser.objects.get(securitycode=code, pk=pk, password=crpassword)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Current Password Wrong"}, status=status.HTTP_404_NOT_FOUND)
			
        serializer = Sl_User_Login_Adminpass(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Admin Password Reset Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Detial view Admin User
class view_detview(APIView):
    def get(self, request, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)
			
        try:
            task = tbl_Adminuser.objects.get(role="Normal Admin")
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_User_updateadmin(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Sum View of Adim
class view_sumviewadmin(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_Adminuser.objects.filter(~Q(role='Dev Admin')).order_by('id')
        serializer = Sl_User_updateadmin(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




# Create Account
class view_createacc(APIView):
    parser_classes = (MultiPartParser, FormParser) 
    def post(self, request, *args, **kwargs):

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

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
                record.accountimageurl = 'https://s3.amazonaws.com/poetapp/' + imagename1
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
    parser_classes = (MultiPartParser, FormParser) 
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
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
                record.accountimageurl = 'https://s3.amazonaws.com/poetapp/' + imagename1
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

# Active Sum View Account
class view_actsumacc(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_Accountholders.objects.filter(accountstatus='Active').order_by('id')
        serializer = Sl_User_SumView(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# In Ative Sum View Account
class view_inactsumacc(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_Accountholders.objects.filter(accountstatus='In-Active').order_by('id')
        serializer = Sl_User_SumView(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Det View Account
class view_detailacc(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)



        try:
            task = tbl_Accountholders.objects.get(pk=pk)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_User_Register(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Delete Account
class view_deletacc(APIView):
    def delete(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)



        try:
            task = tbl_Accountholders.objects.get(pk=pk)
            image1 = task.userimage.name
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

# Update Account Status
class view_activeorinavtive(APIView):
    parser_classes = (MultiPartParser, FormParser) 
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_Accountholders.objects.get(pk=pk)
        except tbl_Accountholders.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_User_ActiveorInactive(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Comment Excecuted Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create Image
class view_uploadimage(APIView):
    parser_classes = (MultiPartParser, FormParser) 
    def post(self, request, *args, **kwargs):

        # conn = S3Connection(config.aws_access_key_id, config.aws_secret_access_key)
        # bucket = conn.get_bucket('poetapp')
        # for key in bucket.list():
        #     print(key.name)

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_image(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            # transfer = S3Transfer(boto3.client('s3', 'us-east-1', 
            #                                 aws_access_key_id = config.aws_access_key_id,
            #                                 aws_secret_access_key=config.aws_secret_access_key))
            session = boto3.session.Session()
            client = session.client('s3', 
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)


            local_path =os.path.join(BASE_DIR, "media/")
            image = record.templateimage.name
            local_image_name = str(image)
            full_path_to_file =os.path.join(local_path, local_image_name) 
            print(full_path_to_file)
            remake = str(record.id)
            updatefile = str.replace(local_image_name, local_image_name, remake)
            imagename1 = "TemplateImage_" + str(updatefile) +".jpg"
            #transfer.upload_file(full_path_to_file, 'poetapp', imagename1, extra_args={'ACL': 'public-read'})
            client.upload_file(full_path_to_file,  # Path to local file
                                config.aws_bucket_name,  # Name of Space
                                imagename1)  # Name for remote file
            client.put_object_acl( ACL='public-read', Bucket=config.aws_bucket_name, Key=imagename1 ) 
            os.remove(os.path.join(local_path, image))
            record.templateimage = imagename1
            record.templateimageurl = 'https://s3.amazonaws.com/poetapp/' + imagename1
            record.status = "True"
            record.save()
            return Response({"Message":"Image Upload Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Image
class view_updatimage(APIView):
    parser_classes = (MultiPartParser, FormParser) 
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_ImageTemplates.objects.get(pk=pk)
        except tbl_ImageTemplates.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_image(task, data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region,
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)

            local_path =os.path.join(BASE_DIR, "media/")
            image = record.templateimage.name
            local_image_name = str(image)
            full_path_to_file =os.path.join(local_path, local_image_name) 
            print(full_path_to_file)
            remake = str(record.id)
            updatefile = str.replace(local_image_name, local_image_name, remake)
            imagename1 = "TemplateImage_" + str(updatefile) +".jpg"
            client.upload_file(full_path_to_file,  # Path to local file
                                config.aws_bucket_name,  # Name of Space
                                imagename1)  # Name for remote file
            client.put_object_acl( ACL='public-read', Bucket=config.aws_bucket_name, Key=imagename1 ) 
            os.remove(os.path.join(local_path, image))
            record.templateimage = imagename1
            record.templateimageurl = 'https://s3.amazonaws.com/poetapp/' + imagename1
            record.status = "True"
            record.save()
            return Response({"Message":"Image Updated Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Remove Image
class view_removeimage(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_ImageTemplates.objects.get(pk=pk)
            image1 = task.templateimage
        except tbl_ImageTemplates.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    config.aws_region, 
                                    aws_access_key_id=config.aws_access_key_id,
                                    aws_secret_access_key=config.aws_secret_access_key)

            client.delete_object(Bucket=config.aws_bucket_name, Key=image1)  # Name for remote file
            task.delete()
            return Response({"Message":"Image Removed"},status=status.HTTP_200_OK)
        except:
            task.delete()
            return Response({"Message":"Image Removed"},status=status.HTTP_200_OK)

# get Image for poet
class view_getimagepoet(APIView):
    def get(self, request, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_ImageTemplates.objects.filter(status='True')
        serializer = Sl_Poet_image(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# get all Image 
class view_getallimage(APIView):
    def get(self, request, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_ImageTemplates.objects.all()
        serializer = Sl_Poet_image(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Create Competition
class view_createcomp(APIView):
    def post(self, request, *args, **kwargs):

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Comp_all(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            return Response({"Message":"Competition Create Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Competition
class view_updatecomp(APIView):
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_CompetitionDetails.objects.get(pk=pk)
        except tbl_CompetitionDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Comp_all(task, data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            return Response({"Message":"Competition Update Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sum View Upcoming Competition
class view_sumcompupcomig(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_CompetitionDetails.objects.filter(status='Upcoming')
        serializer = Sl_Comp_SumView(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Sum View for On Going Competition
class view_sumcompongng(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_CompetitionDetails.objects.filter(status='Ongoing')
        serializer = Sl_Comp_SumView(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Sum View Finish Competition
class view_sumcompcomp(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_CompetitionDetails.objects.filter(status='Finish')
        serializer = Sl_Comp_SumView(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Det View completed Competition
class view_detailcompc(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_CompetitionDetails.objects.get(pk=pk)
        except tbl_CompetitionDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_competitiondetview(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Delete Competition
class view_deletecomp(APIView):
    def delete(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)


        try:
            task = tbl_CompetitionDetails.objects.get(pk=pk)
        except tbl_CompetitionDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({"Message":"Competition Deleted"},status=status.HTTP_200_OK)


# Active Sum view Complaint Poet
class view_sumviewcomplact(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_ComplaintDetails.objects.filter(status='Active').order_by('id')
        serializer = Sl_Poet_sumviewcomplaint(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Block Sum view Complaint Poet
class view_sumviewcomplblk(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_ComplaintDetails.objects.filter(status='Block').order_by('id')
        serializer = Sl_Poet_sumviewcomplaint(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Complaint Detview 
class view_complaindetview(APIView):
    def get(self, request, pk, *args, **kwargs): 
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try: 
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            serializer = Sl_Poet_detview(task)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"Poet is not found"}, status=status.HTTP_404_NOT_FOUND)

        complain = tbl_ComplaintDetails.objects.filter(postid=pk).order_by('id')
        serializer1 = Sl_Poet_complaint(complain, many=True)

        return Response({ "PoetDetails": serializer.data, "Complaints": serializer1.data }, status=status.HTTP_200_OK)

# Block Post
class view_blkpost(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            task.poststatus = 'Block'
            task.save()
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"Poet is not found"}, status=status.HTTP_404_NOT_FOUND)

        complain = tbl_ComplaintDetails.objects.filter(postid=pk).order_by('id')
        for eachdata in complain:
            eachdata.status= 'Block'
            eachdata.save()
        
        return Response({"Message":"Post Block Successfully"}, status=status.HTTP_201_CREATED)

# Unblock Post
class view_unblkpost(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PoetDetails.objects.get(pk=pk)
            task.poststatus = 'Active'
            task.save()
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"Poet is not found"}, status=status.HTTP_404_NOT_FOUND)

        complain = tbl_ComplaintDetails.objects.filter(postid=pk).order_by('id')
        for eachdata in complain:
            eachdata.status= 'Active'
            eachdata.save()
        
        return Response({"Message":"Post Un-Block Successfully"}, status=status.HTTP_201_CREATED)

# Delete Complaint 
class view_deletecomplaint(APIView):
    def delete(self, request, pk, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_ComplaintDetails.objects.get(pk=pk)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"Poet is not found"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({"Message":"Complain Delete Successfully"}, status=status.HTTP_201_CREATED)



# Create Payment
class view_createpayment(APIView):
    def post(self, request, pk, *args, **kwargs):

        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_WinnerDetails.objects.get(pk=pk)
        except tbl_WinnerDetails.DoesNotExist:
            return Response({"Error":"Winner ID is not found"}, status=status.HTTP_404_NOT_FOUND)
   
        serializer = Sl_Poet_paymentall(data=request.data)
        if serializer.is_valid():
            serializer.save()
            task.status = "Paid"
            task.save()
            return Response({"Message":"Payment Done Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Payment
class view_updatepayment(APIView):
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PaymentDetails.objects.get(pk=pk)
        except tbl_PaymentDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_paymentall(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Payment Update Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sum View Payment
class view_paidsumpayment(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_PaymentDetails.objects.all().order_by('id')
        serializer = Sl_Poet_sumviewpayment(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Det View Payment
class view_detailpayment(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PaymentDetails.objects.get(pk=pk)
        except tbl_PaymentDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_paymentall(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Delete Payment
class view_deletepayment(APIView):
    def delete(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_PaymentDetails.objects.get(pk=pk)
        except tbl_PaymentDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)
    
        task.delete()
        return Response({"Message":"Payment list Deleted"},status=status.HTTP_200_OK)
    


# Create Winner
class view_createwinner(APIView):
    def post(self, request, *args, **kwargs):

        serializer = Sl_Poet_winnerall(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Winner Generate Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Winner
class view_updatewinner(APIView):
    def put(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_WinnerDetails.objects.get(pk=pk)
        except tbl_WinnerDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_winnerall(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Winner Update Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Paid Sum View Winner
class view_paidsumwinner(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_WinnerDetails.objects.filter(status='Paid').order_by('id')
        serializer = Sl_Poet_sumviewwinnder(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Un Paid Sum View Winner
class view_unpaidsumwinner(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        task = tbl_WinnerDetails.objects.filter(status='Un-Paid').order_by('id')
        serializer = Sl_Poet_sumviewwinnder(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Det View Winner
class view_detailwinner(APIView):
    def get(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_WinnerDetails.objects.get(pk=pk)
        except tbl_WinnerDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sl_Poet_winnerall(task)
       
        try:
            task = tbl_PoetDetails.objects.get(pk=task.postid_id)
        except tbl_PoetDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer1 = Sl_Poet_detview(task)

        return Response({ "Data": serializer.data, "PoetDetails": serializer1.data }, status=status.HTTP_200_OK)

# Delete Winner
class view_deletewinner(APIView):
    def delete(self, request, pk, *args, **kwargs):
        code = request.META.get('HTTP_SECURITYCODE', None)
        try:
            tbl_Adminuser.objects.get(securitycode=code)
        except tbl_Adminuser.DoesNotExist:
            return Response({"Error":"Invalid Security Token"}, status=status.HTTP_404_NOT_FOUND)

        try:
            task = tbl_WinnerDetails.objects.get(pk=pk)
        except tbl_WinnerDetails.DoesNotExist:
            return Response({"Error":"ID is not found"}, status=status.HTTP_404_NOT_FOUND)
    
        task.delete()
        return Response({"Message":"Winner list Deleted"},status=status.HTTP_200_OK)
    


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
        
        pickup_records=[]

        task = tbl_Notification.objects.filter().order_by('-createdate')
        print(task)
        for each in task:
            notitype = each.notificationtype
            if notitype == "Public":
                record ={"id": each.id, "notificationtitle":each.notificationtitle, "notificationdesc":each.notificationdesc, "notificationtype":each.notificationtype, "assignto":each.assignto, "status":each.status, "createdate":each.createdate  }
                pickup_records.append(record)
            elif notitype == "NotPublic":
                if each.assignto == pk:
                    record ={"id": each.id, "notificationtitle":each.notificationtitle, "notificationdesc":each.notificationdesc, "notificationtype":each.notificationtype, "assignto":each.assignto, "status":each.status, "createdate":each.createdate  }
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
    