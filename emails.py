from flask_mail import Message
from config import mail, app
import os

def send_email(recipients, pdf_file):
    # Create a message object
    msg = Message(subject = "Diabetic Retinopathy Detection - Report", 
                  sender=("Diabetic Retinopathy Detection Team",os.getenv('EMAIL_ADDRESS')), 
                  recipients=[recipients])
    
    msg.html = """
    <h1>Diabetic Retinopathy Detection - Report</h1>
    <p>Dear User,</p>
    <p>Attached is the report for the Diabetic Retinopathy Detection.</p>
    <p>Thank you for using our service.</p>
    <p>Best Regards,</p>
    <p>Diabetic Retinopathy Detection Team</p>
"""

    # Attach the PDF file to the message
    with app.open_resource(pdf_file) as fp:
        msg.attach('DR-Report', 'application/pdf', fp.read())

    # Send the email
    mail.send(msg)

    return 'Email sent successfully!'
