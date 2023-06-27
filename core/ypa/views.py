from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import User, ApiKey
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from urllib import response
from googleapiclient.discovery import build
from maincodes import generate_result, generate_pdf, send_email_with_attachment
import pandas as pd
import os
import io
import csv
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()

# youtubeapikey = os.environ.get('youtubeapikey')
# youtube = build("youtube", "v3", developerKey= youtubeapikey)

def signuppage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        youtubeapikey = request.POST['youtubeapikey']

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

@login_required(login_url='login')
def getoutput(request):
    if request.method == "POST":
        url = request.POST["videoid"]
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        videoid = query_params.get('v', [''])[0]

        key = ApiKey.objects.get(user = request.user)
        youtube = build("youtube", "v3", developerKey= key.youtube_api_key)
        pdf_content = generate_pdf(youtube, videoid)

        username = request.user.username
        recipient = User.objects.get(username=username)
        recipient_email = recipient.email
        subject = f"Hey {username}! Your Report is Out! Check it Now"
        message = f"We have analyzed your video ({videoid}), and this is the result!"
        send_email_with_attachment(videoid,'projectwilsen@gmail.com', os.environ.get('email_pass'), recipient_email, subject, message, pdf_content)
        return redirect('home')
    else:
        return render(request,"home.html")


