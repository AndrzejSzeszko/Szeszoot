#!/usr/bin/python3.7
from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/game/<int:game_pk>/', consumers.MasterGamePanelConsumer),
]
