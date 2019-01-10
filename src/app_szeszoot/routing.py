#!/usr/bin/python3.7
from django.urls import path
from . import consumers


websocket_urlpatterns = [
    # path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
    # path('ws/game_master_panel/<int:quiz_pk>/<int:game_pk>/', consumers.MasterGamePanelConsumer),
    path('ws/game/<int:game_pk>/', consumers.MasterGamePanelConsumer),
    # path('ws/player_panel/<int:game_pk>/', consumers.PlayerPanelConsumer),
]
