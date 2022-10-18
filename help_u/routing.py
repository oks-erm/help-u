from django.urls import path

from messenger.consumers import ChatConsumer

websocket_urlpatterns = [path("", ChatConsumer.as_asgi())]