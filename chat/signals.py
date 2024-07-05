from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Messages
from django.shortcuts import render,redirect
from django.dispatch import Signal, receiver
from channels.layers import get_channel_layer
from .consumers import ChatRoomConsumer
from asgiref.sync import async_to_sync

@receiver(signal=post_save,sender=Messages)
def post_save_handler(sender,instance,created,**kwargs):
    if created:
        print(f"Sender: {sender}, Instance : {instance} Message: Message created (post_save)")


    
    
