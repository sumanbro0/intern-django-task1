from django.conf import settings
from django.core.mail import send_mail


def send_otp(username, email, otp):
        subject = 'Welcome to my blog'
        message = f'Hi {username}, thank you for registering in our blog. Your OTP is {otp}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list )