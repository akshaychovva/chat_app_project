import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Userprofile
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        users_id = self.scope['path_remaining']
        user_ids = users_id.split('/')
        self.roomname = f'{max(user_ids)}_{min(user_ids)}'
        self.room_group_name = self.roomname
        status = True
        userprofile = User.objects.get(id=user_ids[0])
        self.userprofile = userprofile.userprofile
        self.update_user_status(status)
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': status}))

    def disconnect(self, code):
        #user offline
        status = False
        self.update_user_status(status)
        self.send(text_data=json.dumps({"status": status}))
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text["message"]
        username = json_text['username']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message,
                'username': username
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({"message": message}))

    # @database_sync_to_async
    def update_user_status(self, status):
        self.userprofile.user_online_status = status
        self.userprofile.save()
        
