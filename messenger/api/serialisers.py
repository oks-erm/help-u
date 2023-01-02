from rest_framework import serializers
from messenger.models import Message, Conversation
from main.serialisers import CustomUserSerializer
from main.models import CustomUser


class ConversationSerializer(serializers.ModelSerializer):
    """
    ConversationSerializer is a serializer class for the Conversation model.
    """
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
        """
        Test that get_last_message method returns the last message
        in the conversation.
        """
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data

    def get_other_user(self, obj):
        """
        Test that get_other_user method returns the user in the
        conversation who is not the authenticated user.
        """
        ids = obj.name[4:].split("_")
        context = {}
        for user_id in ids:
            if int(user_id) != self.context["user"].id:
                other_user = CustomUser.objects.get(id=user_id)
                return CustomUserSerializer(other_user, context=context).data


class MessageSerializer(serializers.ModelSerializer):
    """
    MessageSerializer is a serializer class for the Message model.
    """
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
        """
        Test that method returns the ID of the Conversation
        object as a string.
        """
        return str(obj.conversation.id)

    def get_from_user(self, obj):
        """
        Test that method returns the serialized data for the
        CustomUser object that sent the message.
        """
        return CustomUserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        """
        Test that method returns the serialized data for the
        CustomUser object that the message was sent to.
        """
        return CustomUserSerializer(obj.to_user).data
