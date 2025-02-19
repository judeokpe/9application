import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from django.utils import timezone
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        me = self.scope["user"]
        print('CURRENTLY LOGGED IN', me)
        
        if not me.is_anonymous:# user is logged in
            self.user_group_name = f"user_group_{me.id}"
            
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            
            await self.accept()#only accept connection if user is logged in
        else:# user is not logged in
            raise DenyConnection('Authentication failed')
        

    async def disconnect(self, close_code):
        print('websocket disconnected')
        await super().disconnect(code=close_code)

    async def receive(self, text_data):
        rd = json.loads(text_data)
        action = rd.get('action', None)
        
        user = self.scope['user']
        receiver_id = rd.get('receiver_id', None)
        
        
        if action == 'chat_message' and receiver_id != user.id:
            message = rd.get('message_body')

            created_msg = await self.create_chat_message(receiver_id, message)
            my_response = {
                'message_body': message,
                'sender_id': str(user.id),
                'receiver_id': str(receiver_id),
                'timestamp': timezone.now().isoformat(),
                'created_msg_id': getattr(created_msg, 'id', None),
                'action': 're_message'
            }
        

            await self.channel_layer.group_send(
                f'user_group_{receiver_id}',
                {
                    'type': 'chat.message',
                    'message': my_response
                }
            )
            
            
    @database_sync_to_async
    def create_chat_message(self, receiver, msg):
        sender= self.scope['user']

        thread, created = Thread.threadm.get_or_new(sender, receiver)

        if thread:
            chat_message, message = ChatMessage.chatm.craete_chat(sender, receiver, msg, thread)
            return chat_message
        
        print('Error: Invalid thread')
        return thread
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))