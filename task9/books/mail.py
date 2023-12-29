from django.conf import settings
from django.core.mail import send_mail


def send_verification(username, email, url):
        subject = 'set your new password'
        message = f'Hi {username}, Here is your password reset link {url}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list )