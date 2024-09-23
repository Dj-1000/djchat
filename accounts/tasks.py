from djhome.celery import app
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import time

@app.task
def send_mail_task(user,message):
    time.sleep(10)
    send_mail(
    subject=f'''
Dear {user.first_name},

Thank you for joining RTC Chat App, your personalized platform for seamless one-on-one conversations!

We’re excited to have you with us. Whether you’re chatting with friends, family, or colleagues, our platform is designed to make private communication simple and efficient.

If you have any questions or need assistance, don’t hesitate to ask. We’re here to ensure you have an enjoyable and smooth chat experience.


Warm regards,
RTC Support Team
''',
    from_email = settings.EMAIL_HOST_USER,
    message = message,
    recipient_list=[user.email],
    fail_silently=False,
)
    
# @app.task
# def add(value1,value2):
#     sum = value1 + value2
#     print(f"Sum of {value1} and {value2} = {sum}")



