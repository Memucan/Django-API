from django.shortcuts import render
import schedule
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from.models import *


def emailjob():    
    emailid = "akash.ndroid@gmail.com"
    message = render_to_string('sample.html', 
    {
        'taskname': "task",
        'assgnto': "assign",
        'inviteby': "createbyname",
        'schdate': "scheduledate",
        'address': "inspectionaddress",
        'buyer': "buyer",
        'supplier': "supplier",
        'factory': "factory",
        'inspector': "inspector",
        'Status': "status"
    })
    mail_subject = "sample mail"
    to_email = emailid
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    print("Mail sent")


def movjob():
    print("movie name")
    account= 'tamilmovie'
    movie_table._meta.db_table = account + '\".\"movie_table'
    mov = movie_table.objects.all()
    for eachlist in mov:
        print(eachlist)

schedule.every(10).seconds.do(movjob) 
while True:
    schedule.run_pending()
    time.sleep(1)

    