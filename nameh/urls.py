from django.urls import path
from .views import chat_view , get_or_create_chatroom

urlpatterns = [
    path("", chat_view, name="chat_view"),
    path("chat/<str:chatroom_name>/", chat_view, name="chatroom"),
    path('chat/<username>', get_or_create_chatroom, name="start-chat"),
]
