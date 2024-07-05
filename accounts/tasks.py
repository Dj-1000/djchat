from djhome.celery import app
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import time
@app.task
def send_mail_task(email,message):
    time.sleep(10)
    send_mail(
    subject='Greetings',
    from_email = settings.EMAIL_HOST_USER,
    message = message,
    recipient_list=[email],
    fail_silently=False,
)
    
@app.task
def add(value1,value2):
    sum = value1 + value2
    print(f"Sum of {value1} and {value2} = {sum}")



