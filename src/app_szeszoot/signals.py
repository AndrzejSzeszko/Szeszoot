#!/usr/bin/python3.7
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Player
import json


@receiver(post_save, sender=Player)
def display_joined_player(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        message = {'from_player_joined_signal': {'nickname': instance.nickname}}
        async_to_sync(channel_layer.group_send)(
            f'master_game_{instance.game.pk}',
            {
                'type': 'join_message',
                'message': message
            }
        )
