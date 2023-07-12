from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q



from .serializers import ResultSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import requests

from .models import User, ApiKey, Result
from django.forms.models import model_to_dict

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
from maincodes_async_await import process_data_and_send_email, get_result, answer_question

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
    

# ASYNCHRONUS (send to email)

# @login_required(login_url='login')
# def getoutput(request):
#     if request.method == "POST":
#         url = request.POST["videoid"]

#         try:
#             key = ApiKey.objects.get(user=request.user)
#             youtubeapikey = key.youtube_api_key
#             if youtubeapikey is None:
#                 youtubeapikey = os.environ.get('youtubeapikey')
#         except:
#             youtubeapikey = os.environ.get('youtubeapikey')

#         username = request.user.username
#         recipient = User.objects.get(username=username)
#         recipient_email = recipient.email

#         async def run_async():
#             await process_data_and_send_email(url, youtubeapikey, username, recipient_email)

#         def run_event_loop():
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             loop.run_until_complete(run_async())
#             loop.close()

#         thread = Thread(target=run_event_loop)
#         thread.start()

#         messages.success(request, 'Processing started.')

#         return redirect('home')

#     else:
#         return render(request, "home.html")


# CHATBOT
# opsi 1

# SOURCE = None

# @login_required(login_url='login')
# def getoutput(request):
#     context = {}
#     if request.method == "POST":
#         url = request.POST["videoid"]

#         try:
#             key = ApiKey.objects.get(user=request.user)
#             youtubeapikey = key.youtube_api_key
#             if youtubeapikey is None:
#                 youtubeapikey = os.environ.get('youtubeapikey')
#         except:
#             youtubeapikey = os.environ.get('youtubeapikey')

#         username = request.user.username
#         recipient = User.objects.get(username=username)
#         recipient_email = recipient.email

#         async def run_async():
#             stats, df, videoid, positive, negative = await get_result(url, youtubeapikey, username, recipient_email)

#             return {
#                 'videoid': videoid,
#                 'videotitle': stats['title'],
#                 'view': stats['viewCount'],
#                 'like': stats['likeCount'],
#                 'comment': stats['commentCount'],
#                 'total_positive_comment': len(df[df['sentiment'] == 'positive']),
#                 'total_negative_comment': len(df[df['sentiment'] == 'negative']),
#                 'total_neutral_comment': len(df[df['sentiment'] == 'neutral']),
#                 'positive_comment': positive,
#                 'negative_comment': negative,
#             }

#         def run_event_loop():
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             context = loop.run_until_complete(run_async())
#             loop.close()

#             messages.success(request, 'Processing started.')
#             return context

#         thread = Thread(target=run_event_loop)
#         thread.start()

#         context = run_event_loop()

#         global SOURCE
#         SOURCE = context
#         print(SOURCE)


#         return render(request, "home.html", context = context)

#     else:
#         return render(request, "home.html")

SOURCE = None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
            stats, df, videoid, positive, negative = await get_result(url, youtubeapikey, username, recipient_email)

            source = {
                # if using API 'user' should be added
                'user': request.user.pk,
                'videoid': videoid,
                'videotitle': stats['title'],
                'view': stats['viewCount'],
                'like': stats['likeCount'],
                'comment': stats['commentCount'],
                'total_positive_comment': len(df[df['sentiment'] == 'positive']),
                'total_negative_comment': len(df[df['sentiment'] == 'negative']),
                'total_neutral_comment': len(df[df['sentiment'] == 'neutral']),
                'positive_comment': positive,
                'negative_comment': negative,
            }

            return source

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        source = loop.run_until_complete(run_async())
        loop.close()
        
        # messages.success(request, 'Processing started.')

        # 1. === SAVE TO GLOBAL VARIABLE ===

        # global SOURCE
        # SOURCE = source
        # print(SOURCE)


        # 2. === SAVE INTO DB USING QUERY === 

        # current_user = request.user
        # videoid = source['videoid']

        # Check if a record with the same videoid exists
        # try:
        #     result = Result.objects.get(user=current_user, videoid=videoid)
        #     print(result)
        # except Result.DoesNotExist:
        #     result = None

        # # If the record exists, update it; otherwise, create a new record
        # if result:
        #     result.videotitle = source['videotitle']
        #     result.view = source['view']
        #     result.like = source['like']
        #     result.comment = source['comment']
        #     result.total_positive_comment = source['total_positive_comment']
        #     result.positive_comment = source['positive_comment']
        #     result.total_negative_comment = source['total_negative_comment']
        #     result.negative_comment = source['negative_comment']
        # else:
        #     result = Result(
        #         user=current_user,
        #         videoid=videoid,
        #         videotitle= source['videotitle'],
        #         view = source['view'],
        #         like = source['like'],
        #         comment = source['comment'],
        #         total_positive_comment = source['total_positive_comment'],
        #         positive_comment = source['positive_comment'],
        #         total_negative_comment = source['total_negative_comment'],
        #         negative_comment = source['negative_comment']
        #     )

        # result.save()

        # 3. SAVE INTO DB USING API

        serializer = ResultSerializer(data = source)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors) 

        return render(request, "home.html", {"source":source})
        # return redirect('chat')

    else:
        return render(request, "home.html")


@login_required(login_url='login')
def chat(request):

    # 1. === USING GLOBAL VARIABLE === 
    # source = SOURCE

    # 2. === USING QUERY DB === 
    # current_user = request.user

    # source = Result.objects.filter(
    #     user=current_user
    # ).latest('created_at')

    # user=source.user
    # videoid=source.videoid
    # videotitle= source.videotitle
    # view = source.view
    # like = source.like
    # comment = source.comment
    # total_positive_comment = source.total_positive_comment
    # positive_comment = source.positive_comment
    # total_negative_comment = source.total_negative_comment
    # negative_comment = source.negative_comment

    # Make the result into dictionary and save it as source
    # sources = model_to_dict(source)

    # 3. === USING API === 

    # token = request.user.auth_token.key
    user = request.user.pk

    api_url = f'http://127.0.0.1:8000/result/{user}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        source = data[-1]
    else:
        print('Error:', response.status_code)
    
    videoid = source['videoid'],
    videotitle= source['videotitle'],
    view = source['view'],
    like = source['like'],
    comment = source['comment'],
    total_positive_comment = source['total_positive_comment'],
    positive_comment = source['positive_comment'],
    total_negative_comment = source['total_negative_comment'],
    negative_comment = source['negative_comment']

    # context = {
    #             # if using API 'user' should be added
    #             'user': request.user.pk,
    #             'videoid': videoid,
    #             'videotitle': stats['title'],
    #             'view': stats['viewCount'],
    #             'like': stats['likeCount'],
    #             'comment': stats['commentCount'],
    #             'total_positive_comment': len(df[df['sentiment'] == 'positive']),
    #             'total_negative_comment': len(df[df['sentiment'] == 'negative']),
    #             'total_neutral_comment': len(df[df['sentiment'] == 'neutral']),
    #             'positive_comment': positive,
    #             'negative_comment': negative,
    #         }

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        answer = answer_question(
            user_input, videoid, videotitle, view, like, comment,
            total_positive_comment, positive_comment, 
            total_negative_comment, negative_comment)

        print(answer)

    return(render(request, "home.html", {"response":answer, "source": source}))


@api_view(['GET','POST'])
def result_list_all(request):

    if request.method == "GET":

        result = Result.objects.all()
        serializer = ResultSerializer(result, many = True)
        
        return JsonResponse(serializer.data, safe = False)
    
    if request.method == "POST":

        serializer = ResultSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def result_list_by_user(request,user):

    try:
        result = Result.objects.filter(user=user)
    except Result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResultSerializer(result, many = True)
        return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = ResultSerializer(drink, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     drink.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
