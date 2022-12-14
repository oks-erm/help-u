import json
from uuid import UUID
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from messenger.api.serialisers import MessageSerializer
from main.serialisers import CustomUserSerializer
from main.models import CustomUser
from .models import Conversation, Message


class UUIDEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for UUID objects.
    """
    def default(self, obj):
        """
        Encodes a UUID object as a hexadecimal string.
        """
        if isinstance(obj, UUID):
            # if the obj is uuid, it returns the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to send chat messages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def connect(self, *args):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            return

        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['q']}"
        split_name = (list(map(int, self.conversation_name[4:].split("_"))))
        split_name.sort()
        # pylint: disable=no-member
        self.conversation, created = Conversation.objects.get_or_create(
            name=f"conv{split_name[0]}_{split_name[1]}"
        )
        for user_id in split_name:
            self.conversation.members.add(CustomUser.objects.get(id=user_id))

        # because group_add is asynchronous, it would not work
        # without being converted to a synchronous function
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        messages = self.conversation.messages.all().order_by(
            "-timestamp")[0:50]
        user = self.get_receiver()
        message_count = self.conversation.messages.all().count()
        if self.user in self.conversation.members.all():
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
            # pylint: disable=no-member
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
                    "user_id": self.user.id,
                    "message": MessageSerializer(message).data,
                },
            )

            notification_group_name = str(
                self.get_receiver().id) + "__notifications"
            async_to_sync(self.channel_layer.group_send)(
                notification_group_name,
                {
                    "type": "new_message_notification",
                    "name": self.user.id,
                    "message": MessageSerializer(message).data,
                },
            )

        if message_type == "read_messages":
            messages_to_me = self.conversation.messages.filter(
                to_user=self.user)
            messages_to_me.update(read=True)

            # Update the unread message count
            # pylint: disable=no-member
            unread_count = Message.objects.filter(
                to_user=self.user, read=False).count()
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
        # private notification group
        self.notification_group_name = str(self.user.id) + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # count of unread messages
        # pylint: disable=no-member
        have_notifications = Message.objects.filter(
            to_user=self.user, read=False)
        unread_count = have_notifications.count()
        from_user = [item.from_user.id for item in have_notifications]
        each = list(
            {(fr_user, have_notifications.filter(from_user=fr_user).count())
             for fr_user in from_user}
            )
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
