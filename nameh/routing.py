from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chat/<chatroom_name>/", ChatroomConsumer.as_asgi()),
    path("ws/online-status/" , onlineStatusConsumer.as_asgi()) ,
]
