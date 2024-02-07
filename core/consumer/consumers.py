# core/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Message
from core.queries import MessageType

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["user"].unqname
        self.receiver = self.scope.get("query_string").decode("utf-8").split("=")[1]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']

        await self.save_message(content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'content': content,
                'sender': self.sender,
                'receiver': self.receiver,
            }
        )

    async def chat_message(self, event):
        content = event['content']
        sender = event['sender']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'content': content,
            'sender': sender,
            'receiver': receiver,
        }))

    @database_sync_to_async
    def save_message(self, content):
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content=content
        )
