from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Room
from django.db.models import Q
from .models import Messages


User = get_user_model()

def index(request):
    return render(request, 'chat/index.html',context={})

@login_required
def room(request,other_user_id):
    user_id = request.user.id
    other_user_id = other_user_id

    user = User.objects.filter(id = user_id).first()
    other_user = User.objects.filter(id = other_user_id).first()

    if user and other_user:
        rooms_with_user = Room.objects.filter(member=user).filter(member=other_user).first()
        if rooms_with_user:
            return redirect(reverse('chat_view',kwargs={"room_id" : rooms_with_user.id}))
            
         
        else:
            room = Room()
            room.save()
            room.member.add(user,other_user)
            return redirect(reverse('chat_view',kwargs={"room_id" : room.id}))

def chat_view(request,room_id):
    prev_messages = Messages.objects.filter(room__id = room_id).order_by('-created_at')
    context = {
        'room_id': room_id,
        'prev_messages' : prev_messages
    }
    return render(request,'chat/chatroom.html',context=context)
    
