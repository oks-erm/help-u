from django.urls import path

from messenger.consumers import ChatConsumer

websocket_urlpatterns = [path("messages/chat/<q>", ChatConsumer.as_asgi())]
