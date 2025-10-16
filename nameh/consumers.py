# consumers.py
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import ChatGroup, GroupMessage
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import json

class ChatroomConsumer(WebsocketConsumer):

    def update_online_count(self):
        # show the real number of users in the M2M
        online_count = self.chatroom.users_online.count() - 1

        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)


    def online_count_handler(self, event):
        online_count = event['online_count']

        context = {
            'online_count': online_count,
            'chat_group': self.chatroom,
        }
        html = render_to_string("nameh/partials/online_count.html", context)
        # send HTML string; client JS will insert it into the DOM
        self.send(text_data=html)


    def connect(self):
        self.user = self.scope.get('user')
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(self.chatroom_name, self.channel_name)
        self.accept()

        # only add if authenticated and not already in the M2M
        if getattr(self.user, "is_authenticated", False) and self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.chatroom_name, self.channel_name)

        # remove user when they disconnect (if authenticated)
        if getattr(self.user, "is_authenticated", False) and self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()


    def receive(self, text_data):
        # only accept JSON messages like {"body": "..."}
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        body = data.get('body')
        if not body:
            return

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        # broadcast to the group by message id so other consumers can render it with their context
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)


    def message_handler(self, event):
        message_id = event.get('message_id')
        if not message_id:
            return
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_group': self.chatroom
        }
        html = render_to_string("nameh/partials/chat_message_p.html", context=context)
        self.send(text_data=html)


class onlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.group_name = 'online-status'
        self.group = get_object_or_404(ChatGroup, group_name=self.group_name)

        if self.user not in self.group.users_online.all():
            self.group.users_online.add(self.user)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        self.online_status()

    def disconnect(self, close_code):
        if self.user in self.group.users_online.all():
            self.group.users_online.remove(self.user)

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        self.online_status()

    def online_status(self):
        event = {
            'type': 'online_status_handler'
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, event
        )

    def online_status_handler(self, event):
        online_users = self.group.users_online.exclude(id=self.user.id)

        context = {
            'online_users': online_users,

        }
        html = render_to_string("nameh/partials/online_status.html", context=context)
        self.send(text_data=html)