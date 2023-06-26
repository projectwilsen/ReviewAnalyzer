import os
import ssl
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv

load_dotenv()

email_sender = 'projectwilsen@gmail.com'
email_password = os.environ.get('email_pass')
print(email_password)
email_reciever = 'wilsenp@gmail.com'

subject = 'Your Report is Out! Check it Now'
body  = """
We have analyzed your video, and this is the result!
"""

em = EmailMessage()

em['From'] = email_sender
em['To'] = email_reciever
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender, email_reciever, em.as_string())
