from django.urls import path
from .views import chat_view

urlpatterns = [
    path("", chat_view, name="chat_view"),
    path("chat/<str:chatroom_name>/", chat_view, name="chatroom"),
]
