#!/usr/bin/python3.7
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Player
import json


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave from group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     async def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to the room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))


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


# class PlayerPanelConsumer(WebsocketConsumer):
#     def connect(self):
#         self.game_pk = self.scope['url_route']['kwargs']['game_pk']
#         self.player_group_name = f'player_game_{self.game_pk}'
#
#         # Join game group
#         async_to_sync(self.channel_layer.group_add)(
#             self.player_group_name,
#             self.channel_name
#         )
#
#     def disconnect(self, close_code):
#
#         # Leave game group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.player_group_name,
#             self.channel_name
#         )
#
#     # Receive data from WebSocket
#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to game group
#         async_to_sync(self.channel_layer.group_send)(
#             self.player_group_name,
#             {
#                 'type': 'next_question_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from game group
#     def next_question_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
