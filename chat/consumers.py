from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Room,Messages
from django.db.models import Q
from django.contrib.auth.models import User

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print("In connect :",self.room_name,self.room_group_name)

        self.user = self.scope['user']
        self.room = await database_sync_to_async(Room.objects.get)(id=self.room_name)
        self.other_user = await self.get_other_user(room=self.room)

        if self.other_user:
            print(f"User 1 :{self.user} Other User : {self.other_user}")

        if not self.user.is_authenticated:
            print("User is anonymous")
            return await self.close()
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
    
        if message:
            await database_sync_to_async(Messages.objects.create)(
                room = self.room,
                content = message,
                sent_by = self.user,
                sent_to = self.other_user
            )
        # Send message to room group
        print("Sending messages to room: ",message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "current_user":await self.get_current_user(self.user),
                "sent_by": await self.get_sent_by(message)
            })


    # Receive message from room group
    async def chat_message(self, event):
        msg = event["message"]

        print("Recieved from group:",msg)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": msg,
            "sent_by": await self.get_sent_by(msg),
            "current_user":await self.get_current_user(self.user)
        }))



    @database_sync_to_async
    def get_other_user(self,room):
        return list(room.member.all().exclude(id = self.user.id))[0]
        
    @database_sync_to_async
    def get_sent_by(self,message):
        msg = Messages.objects.filter(content=message).first()
        return msg.sent_by.first_name
    
    @database_sync_to_async
    def get_current_user(self,user):
        msg = User.objects.filter(id = user.id).first()
        return msg.first_name