from django.urls import path
from .views import MessagesView
from .consumers import ChatConsumer

app_name = 'messenger'

urlpatterns = [
    path('', MessagesView.as_view(), name='conv_list'),
    path('chat/<path:path>', MessagesView.as_view(), name='messages_with_path')
]
