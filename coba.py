import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from reportlab.pdfgen import canvas
from io import BytesIO
import os

from dotenv import load_dotenv

load_dotenv()

def generate_pdf():
    # Create a BytesIO object to store the PDF content
    buffer = BytesIO()

    # Create a new canvas
    c = canvas.Canvas(buffer)

    # Draw on the canvas
    c.drawString(100, 750, "Hello, World!")

    # Save the canvas content into the buffer
    c.save()

    # Seek to the beginning of the buffer
    buffer.seek(0)

    # Retrieve the PDF content as bytes
    pdf_content = buffer.getvalue()

    print("PDF generated successfully!")

    # Return the PDF content
    return pdf_content

def send_email_with_attachment(sender_email, sender_password, recipient_email, subject, message, attachment_content):
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
        "attachment; filename=my_pdf.pdf"
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

# Example usage
sender_email = 'projectwilsen@gmail.com'
sender_password = os.environ.get('email_pass')
recipient_email = 'wilsenp@gmail.com'
subject = 'Your Report is Out! Check it Now'
message = """
We have analyzed your video, and this is the result!
"""

pdf_content = generate_pdf()
send_email_with_attachment(sender_email, sender_password, recipient_email, subject, message, pdf_content)
