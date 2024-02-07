"""
ASGI config for team_chat_be project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.consumers.consumers import ChatConsumer
from core.routing import websocket_urlpatterns  # Adjust the import path based on your project structure

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_chat_be.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                # [
                #     path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
                # ]
                websocket_urlpatterns

            )
        ),
    }
)

