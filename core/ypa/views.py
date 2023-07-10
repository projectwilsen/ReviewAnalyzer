from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User, ApiKey

from googleapiclient.discovery import build

import pandas as pd
import os
import io
import csv

from dotenv import load_dotenv

from urllib import response
from urllib.parse import urlparse, parse_qs

import asyncio
from threading import Thread

from maincodes import generate_pdf, send_email_with_attachment
from maincodes_async_await import process_data_and_send_email

import matplotlib
matplotlib.use('Agg')  # Set the Agg backend
import matplotlib.pyplot as plt

load_dotenv()


def signuppage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        youtubeapikey = request.POST['youtubeapikey']
        print(username,email,password,password2)
        print(youtubeapikey)


        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username Taken!")
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email Taken!")
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    ApiKey.objects.create(
                    user=user,
                    youtube_api_key=youtubeapikey
                    )

                    messages.success(request, "Registered!")
                    return redirect('login')
        else:
            messages.error(request, "Passwords Don't Match!")
            return redirect('signup')
        
    return render(request, 'signup.html')


def loginpage(request):
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials!")
            print("user not found")
            return redirect('login')
    
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

# SYNCHRONUS

# @login_required(login_url='login')
# def getoutput(request):
#     if request.method == "POST":
#         url = request.POST["videoid"]
#         parsed_url = urlparse(url)
#         query_params = parse_qs(parsed_url.query)

#         videoid = query_params.get('v', [''])[0]

#         try:
#             key = ApiKey.objects.get(user = request.user)
#             youtubeapikey = key.youtube_api_key
#             if youtubeapikey == None:
#                 youtubeapikey = os.environ.get('youtubeapikey')
#         except:
#             youtubeapikey = os.environ.get('youtubeapikey')

#         youtube = build("youtube", "v3", developerKey= youtubeapikey)
#         pdf_content = generate_pdf(youtube, videoid)

#         username = request.user.username
#         recipient = User.objects.get(username=username)
#         recipient_email = recipient.email
#         subject = f"Hey {username}! Your Report is Out! Check it Now"
#         message = f"We have analyzed your video ({videoid}), and this is the result!"
#         send_email_with_attachment(videoid,'projectwilsen@gmail.com', os.environ.get('email_pass'), recipient_email, subject, message, pdf_content)
#         return redirect('home')
#     else:
#         return render(request,"home.html")
    

# ASYNCHRONUS

@login_required(login_url='login')
def getoutput(request):
    if request.method == "POST":
        url = request.POST["videoid"]

        try:
            key = ApiKey.objects.get(user=request.user)
            youtubeapikey = key.youtube_api_key
            if youtubeapikey is None:
                youtubeapikey = os.environ.get('youtubeapikey')
        except:
            youtubeapikey = os.environ.get('youtubeapikey')

        username = request.user.username
        recipient = User.objects.get(username=username)
        recipient_email = recipient.email

        async def run_async():
            await process_data_and_send_email(url, youtubeapikey, username, recipient_email)

        def run_event_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_async())
            loop.close()

        thread = Thread(target=run_event_loop)
        thread.start()

        # Clear previous labels and plots in Matplotlib
        # plt.clf()
        # plt.cla()

        messages.success(request, 'Processing started.')

        return redirect('home')

    else:
        return render(request, "home.html")
