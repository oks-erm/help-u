from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from uuid import UUID
from messenger.api.serialisers import MessageSerializer
from main.serialisers import CustomUserSerializer
from .models import Conversation, Message
from main.models import CustomUser


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def connect(self):
        self.user = self.scope['user']

        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['q']}"
        self.conversation, created = Conversation.objects.get_or_create(
            name=self.conversation_name
            )

        # because group_add is asynchronous, it would not work
        # without being converted to a synchronous function
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        messages = self.conversation.messages.all().order_by("-timestamp")[0:50]
        user = self.get_receiver()
        message_count = self.conversation.messages.all().count()
        self.send_json(
            {
                "type": "last_50_messages",
                "messages": MessageSerializer(messages, many=True).data,
                "to_user": CustomUserSerializer(user).data,
                "has_more": message_count > 50,
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def get_receiver(self):
        ids = self.conversation_name[4:].split("_")
        for user_id in ids:
            if int(user_id) != self.user.id:
                return CustomUser.objects.get(id=user_id)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]

        if message_type == "chat_message":
            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                text=content["message"],
                conversation=self.conversation,
            )

            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "name": self.user.id,
                    "message": MessageSerializer(message).data,
                },
                )

            notification_group_name = str(self.get_receiver().id) + "__notifications"
            async_to_sync(self.channel_layer.group_send)(
                    notification_group_name,
                    {
                        "type": "new_message_notification",
                        "name": self.user.id,
                        "message": MessageSerializer(message).data,
                    },
                )

        if message_type == "read_messages":
            messages_to_me = self.conversation.messages.filter(to_user=self.user)
            messages_to_me.update(read=True)

            # Update the unread message count
            unread_count = Message.objects.filter(to_user=self.user, read=False).count()
            async_to_sync(self.channel_layer.group_send)(
                str(self.user.id) + "__notifications",
                {
                    "type": "unread_count",
                    "unread_count": unread_count,
                },
            )

        return super().receive_json(content, **kwargs)
    
    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)

    def new_message_notification(self, event):
        self.send_json(event)

    def unread_count(self, event):
        self.send_json(event)


class NotificationConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to send notifications.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.notification_group_name = None
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        self.accept()

        self.notification_group_name = str(self.user.id) + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        have_notifications = Message.objects.filter(to_user=self.user, read=False)
        unread_count = have_notifications.count()
        from_user = [item.from_user.id for item in have_notifications]
        each = list({(fr_user, have_notifications.filter(from_user=fr_user).count())
                     for fr_user in from_user})
        self.send_json(
            {
                "type": "unread_count",
                "unread_count": unread_count,
                "each": each,
            }
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_message_notification(self, event):
        self.send_json(event)

    def unread_count(self, event):
        self.send_json(event)
