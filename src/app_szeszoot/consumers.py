#!/usr/bin/python3.7
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class MasterGamePanelConsumer(WebsocketConsumer):
    def connect(self):
        self.game_pk = self.scope['url_route']['kwargs']['game_pk']
        self.master_group_name = f'master_game_{self.game_pk}'
        print(f'Connected {self.game_pk} {self.master_group_name} {self.channel_name}')

        # Join game group
        async_to_sync(self.channel_layer.group_add)(
            self.master_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):

        # Leave game group
        async_to_sync(self.channel_layer.group_discard)(
            self.master_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to game group
        async_to_sync(self.channel_layer.group_send)(
            self.master_group_name,
            {
                'type': 'join_message',
                'message': message
            }
        )

    # Receive message from game group
    def join_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
