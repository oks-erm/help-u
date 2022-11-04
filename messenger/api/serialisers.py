from rest_framework import serializers
from messenger.models import Message, Conversation
from main.serialisers import CustomUserSerializer
from main.models import CustomUser


class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name", "other_user", "last_message", "user")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data

    def get_other_user(self, obj):
        ids = obj.name[4:].split("_")
        context = {}
        for user_id in ids:
            if int(user_id) != self.context["user"].id:
                other_user = CustomUser.objects.get(id=user_id)
                return CustomUserSerializer(other_user, context=context).data


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "text",
            "timestamp",
            "read",
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)

    def get_from_user(self, obj):
        return CustomUserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return CustomUserSerializer(obj.to_user).data