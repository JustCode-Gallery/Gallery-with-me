import random
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    subject = 'Your Email Verification Code'
    message = f'Your verification code is: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
