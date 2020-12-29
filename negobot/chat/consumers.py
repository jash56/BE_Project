import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room_id = data['room_id']
        messages = Message.last_10_messages(room_id)
        content = {
            'command' : 'old_messages',
            'messages': self.messages_to_json(messages),
        }
        return self.send_chat_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room_id = data['room_id']
        message = Message.objects.create(author=author_user, content=data['message'], room_id=room_id)
        content = {
            'command' : 'new_message',
            'message': self.message_to_json(message),
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self, messages):
        result = []
        if messages:
            for message in messages:
                result.append(self.message_to_json(message))
            return result
    
    def message_to_json(self, message):
        time = str(message.timestamp)
        return{
            'author': message.author.username,
            'content': message.content,
            'timestamp': time[11:16],
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message): 
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))