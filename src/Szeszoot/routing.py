#!/usr/bin/python3.7
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter
)
from channels.auth import AuthMiddlewareStack
import app_szeszoot.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app_szeszoot.routing.websocket_urlpatterns
        )
    )
})
