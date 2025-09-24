from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import json


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        async_to_sync( self.channel_layer.group_add)(
            self.chatroom_name , self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )



    def receive(self, text_data):

        data = json.loads(text_data)
        body = data.get('body')
        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )
        context = {
            'message'  : message ,
            'user' : self.user
        }
        html = render_to_string("nameh/partials/chat_message_p.html", context)
        self.send(text_data=html)

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_group': self.chatroom
        }
        html = render_to_string("nameh/partials/chat_message_p.html", context=context)
        self.send(text_data=html)
