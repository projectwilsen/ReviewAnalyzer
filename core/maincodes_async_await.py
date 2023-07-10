from urllib import response
from googleapiclient.discovery import build

from textblob import TextBlob
import nltk

import pandas as pd
import matplotlib.pyplot as plt
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from langchain import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import textwrap
from transformers import pipeline

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from io import BytesIO
from dotenv import load_dotenv, find_dotenv

import asyncio

from urllib.parse import urlparse, parse_qs

import time

load_dotenv()


async def video_stats(youtube, videoIDs, channelID = None, to_csv=False):
    if type(videoIDs) == str:
        videoIDs = [videoIDs]
    
    stats_list = []

    for videoId in videoIDs:
        request = youtube.videos().list(
            part="snippet, statistics, contentDetails",
            id=videoId
        )
        response = request.execute()
        statistics = response['items'][0]['statistics']
        snippet = response['items'][0]['snippet']
        statistics['videoId'] = videoId
        statistics['title'] = snippet['title']
        statistics['description'] = snippet['description']
        statistics['publishedAt'] = snippet['publishedAt']
        statistics['duration'] = response['items'][0]['contentDetails']['duration']
        statistics['thumbnail'] = snippet['thumbnails']['high']['url']
        statistics['channelId'] = channelID
        statistics['likeCount'] = statistics.get('likeCount', 0)

        print(f"Fetched stats for {videoId}")
        stats_list.append(statistics)

    return statistics

def process_comments(response_items, channelID = None, csv_output=False):
    comments = []

    for res in response_items:

        # loop through the replies
        if 'replies' in res.keys():
            for reply in res['replies']['comments']:
                comment = reply['snippet']
                comment['commentId'] = reply['id']
                comments.append(comment)
        else:
            comment = {}
            comment['snippet'] = res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']

            comments.append(comment['snippet'])
        
    keytoremove = ['textDisplay','authorProfileImageUrl','authorChannelUrl','authorChannelId','canRate','viewerRating','likeCount','updatedAt','parentId']
    for i in comments:
        for y in keytoremove:
            del i[y]

    new_comments = []
    for original_dict in comments:
        new_dict = {
            'video_id': original_dict['videoId'],
            'comment_id': original_dict['commentId'],
            'date': original_dict['publishedAt'],
            'author': original_dict['authorDisplayName'],
            'comment_text': original_dict['textOriginal']
        }
        new_comments.append(new_dict)

    new_key = 'channel_id'
    new_value = channelID

    for dictionary in new_comments:
        new_dict = {new_key: new_value}
        new_dict.update(dictionary)
        dictionary.clear()
        dictionary.update(new_dict)

    def sentiment(i):
        blob = TextBlob(i)
        score = blob.sentiment.polarity
        if score == 0:
            sentiment = 'neutral'
        elif score > 0: 
            sentiment = 'positive'
        else:
            sentiment = 'negative'

        return sentiment
    
    for comment in new_comments:
        if type(comment['comment_text']) == 'float':
            comment['sentiment'] == 'no sentiment for numerical values'
        else:
            comment['sentiment'] = sentiment(comment['comment_text'])

    print(f'Finished processing {len(new_comments)} comments.')
    return new_comments

scraped_videos = {}

async def comment_threads(youtube, videoID, channelID=None, to_csv=False):
    
    comments_list = []
    
    try:
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=videoID,
        )
        response = request.execute()
    except Exception as e:
        print(f'Error fetching comments for {videoID} - error: {e}')
        if scraped_videos.get('error_ids', None):
            scraped_videos['error_ids'].append(videoID)
        else:
            scraped_videos['error_ids'] = [videoID]
        return

    comments_list.extend(process_comments(response['items'],channelID))

    # if there is nextPageToken, then keep calling the API
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=videoID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items'],channelID)) 
    
    print(f"Finished fetching comments for {videoID}. {len(comments_list)} comments found.")
    
    if scraped_videos.get(channelID, None):
        scraped_videos[channelID].append(videoID)
    else:
        scraped_videos[channelID] = [videoID]

    comment_df = pd.DataFrame(comments_list)

    return comment_df

async def sentiment_barchart(df):
    sentiment_counts = df['sentiment'].value_counts()
    colors = ['#A93E38']

    # Plotting the bar chart
    plt.bar(sentiment_counts.index, sentiment_counts.values, color = colors)
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis')

    for i, count in enumerate(sentiment_counts.values):
        plt.text(i, count, str(count), ha='center', va='top')

    temp_image = f"temp_plot_{time.time()}.png"  # Unique temporary image file name
    plt.savefig(temp_image)

    return temp_image

def draw_text_with_wrap(canvas, text, x, y, width):
    lines = []
    current_line = ""
    words = text.split()

    for word in words:
        if canvas.stringWidth(current_line + " " + word) < width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word

    if current_line != "":
        lines.append(current_line.strip())

    for line in lines:
        canvas.drawString(x, y, line)
        y -= 15

    return y

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["huggingfacehub_api_token"]

repo_id = "tiiuae/falcon-7b-instruct"  
falcon_llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_new_tokens": 425}
)

rm = 'deepset/roberta-base-squad2'

question_answerer = pipeline("question-answering", model=rm)

async def summary_of_comments(df,things = 'positive'):
    filtered_comment = df[df['sentiment'] == things]
    comment_text = ';'.join(filtered_comment['comment_text']).replace('\n','')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
    comment_doc = text_splitter.create_documents([comment_text])

    output = {}
    for i in comment_doc:
        result = question_answerer(question= f"What {things} things does the user/audience feel?", context= i.page_content) #str(i)
        output[result['answer']] = round(result['score'], 4)
        print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")
        
    keys_set = set(output.keys())
    keys_sentence = '; '.join([key for key in keys_set])
    print(keys_sentence)

    docs = text_splitter.create_documents([keys_sentence])
    print('done splitting')

    chain = load_summarize_chain(falcon_llm, chain_type="map_reduce", verbose=True)
    print(chain.llm_chain.prompt.template)
    print(chain.combine_document_chain.llm_chain.prompt.template)

    output_summary = chain.run(docs)
    wrapped_text = textwrap.fill(
        output_summary, width=100, break_long_words=False, replace_whitespace=False
    )
    print(wrapped_text)

    return wrapped_text


async def generate_pdf(videoid,stats,temp_image,positive,negative):
    
    buffer = BytesIO()

    # Create a new canvas
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set the initial y-coordinate for writing the text
    y = 700

    # Write the video title as the sub title
    header = "Youtube Video Performance Analysis : {}".format(videoid)
    c.setFont('Helvetica-Bold', 18)
    c.drawString(50, y, header)
    y -= 30
    c.setFont('Helvetica-Bold', 14)
    sub_title_1 = "Statistic"
    c.drawString(50, y, sub_title_1)
    c.setFont('Helvetica', 12)
    y -= 30

    # Write specific video stats to the PDF
    stat_labels = {'title': 'Title', 'viewCount': 'Total View',
                   'likeCount': 'Total Like', 'commentCount': 'Total Comment'}
    for key, label in stat_labels.items():
        value = stats.get(key, '')
        text = '{}: {}'.format(label, value)
        c.drawString(50, y, text)
        y -= 15


    y -= 30
    c.setFont('Helvetica-Bold', 14)
    sub_title_2 = "Sentiment Analysis"
    c.drawString(50, y, sub_title_2)

    y -= 30
    c.setFont('Helvetica', 12)

    # Draw the barchart in the PDF
    canvas_width = 612  # Width of the canvas (letter size)
    image_width = 400  # Width of the image

    x = (canvas_width - image_width) / 2
    c.drawImage(temp_image, x=x, y=290, width=image_width, height=255)

    y -= 260
    c.setFont('Helvetica-Bold', 12)
    sub_title_3 = "Summary of Positive Sentiment Comments"
    c.drawString(50, y, sub_title_3)

    y -= 30
    c.setFont('Helvetica', 11)
    y = draw_text_with_wrap(c, positive, 50, y, 500)

    y -= 20
    c.setFont('Helvetica-Bold', 12)
    sub_title_4 = "Summary of Negative Sentiment Comments"
    c.drawString(50, y, sub_title_4)

    y -= 30
    c.setFont('Helvetica', 11)
    y = draw_text_with_wrap(c, negative, 50, y, 500)

    c.showPage()
    c.save()

    buffer.seek(0)

    # Retrieve the PDF content as bytes
    pdf_content = buffer.getvalue()

    print("PDF generated successfully!")


    # Return the PDF content
    return pdf_content, temp_image


async def send_email_with_attachment(videoid,sender_email, sender_password, recipient_email, subject, message, attachment_content):
    # Create a multipart message object
    message_obj = MIMEMultipart()
    message_obj["From"] = sender_email
    message_obj["To"] = recipient_email
    message_obj["Subject"] = subject

    # Add the message body
    message_obj.attach(MIMEText(message, "plain"))

    # Create a MIME base object with the attachment content
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment_content)

    # Encode the attachment with base64
    encoders.encode_base64(part)

    # Set the filename and header for the attachment
    part.add_header(
        "Content-Disposition",
        f"attachment; filename=report_{videoid}.pdf"
    )

    # Attach the attachment to the message object
    message_obj.attach(part)

    # Connect to the SMTP server (Gmail's SMTP server in this example)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Initiate TLS connection
        server.starttls()
        # Login to the email account
        server.login(sender_email, sender_password)
        # Send the email
        server.send_message(message_obj)

    print("Email sent successfully!")


async def process_data_and_send_email(url, youtubeapikey, username, recipient_email):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    videoid = query_params.get('v', [''])[0]

    subject = f"Hey {username}! Your Report is Out! Check it Now"
    message = f"We have analyzed your video ({videoid}), and this is the result!"

    youtube = build("youtube", "v3", developerKey= youtubeapikey)

    stats = await video_stats(youtube, videoid)
    df = await comment_threads(youtube, videoID=videoid)
    temp_image = await sentiment_barchart(df)
    # positive = await summary_of_comments(df,'positive')
    # negative = await summary_of_comments(df,'negative')
    pdf, temp_image_path = await generate_pdf(videoid,stats,temp_image,"positive","negative")
    await send_email_with_attachment(videoid,'projectwilsen@gmail.com', os.environ.get('email_pass'), recipient_email, subject, message, pdf)

    # Remove the temporary image file
    os.remove(temp_image_path)

    return "Process completed successfully."







