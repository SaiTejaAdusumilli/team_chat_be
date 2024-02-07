# your_project/routing.py
from django.urls import path
from core.consumers import ChatConsumer  # Adjust the import path based on your project structure

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
    # Add more WebSocket consumers and paths as needed
]
