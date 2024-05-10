from django.urls import re_path
from . import consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$",consumers.ChatRoomConsumer.as_asgi())
]

# application = ProtocolTypeRouter(
#     {
#         "websocket": AuthMiddlewareStack(
#             URLRouter(websocket_urlpatterns)
#         ),
#     }
# )