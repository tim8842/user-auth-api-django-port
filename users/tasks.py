# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_registration_email(user_email):
    send_mail(
        'Welcome!',
        'Thank you for registering on our platform.',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )