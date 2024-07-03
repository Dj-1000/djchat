from django.urls import path,re_path
from .views import index,room,chat_view
urlpatterns = [
    path('',index,name='index'),
    path('<int:other_user_id>/',room,name='chatroom'),
    path('chat/<uuid:room_id>/',chat_view,name = 'chat_view')
]