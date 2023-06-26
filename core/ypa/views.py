from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from urllib import response
from googleapiclient.discovery import build
from maincodes import generate_result, generate_pdf, send_email_with_attachment
import pandas as pd
import os
import io
import csv
from dotenv import load_dotenv

load_dotenv()

youtubeapikey = os.environ.get('youtubeapikey')
youtube = build("youtube", "v3", developerKey= youtubeapikey)

sender_email = 'projectwilsen@gmail.com'
sender_password = os.environ.get('email_pass')
recipient_email = 'wilsenp@gmail.com'
subject = 'Your Report is Out! Check it Now'
message = """
We have analyzed your video, and this is the result!
"""

def index(request):
    return render(request, 'index.html')

def getoutput(request):
    if request.method == "POST":
        videoid = request.POST["videoid"]
        # youtube = build("youtube", "v3", developerKey=request.POST["youtubeapikey"])
        pdf_content = generate_pdf(youtube, videoid)
        send_email_with_attachment(videoid,sender_email, sender_password, recipient_email, subject, message, pdf_content)
        # messages.success(request, "Report sent successfully!")
        return render(request, 'index.html')
    else:
        return render(request,"index.html")
