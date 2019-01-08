#!/usr/bin/python3.7
from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
    path('ws/game_master_panel/<int:quiz_id>/<int:game_id>/', consumers.MasterGamePanelConsumer),
]
