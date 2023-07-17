from django.urls import path

from .consumers import QueueConsumer

websocket_urlpatterns = [
    path('ws/', QueueConsumer.as_asgi()),
]