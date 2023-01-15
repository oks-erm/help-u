"""
Models of the Messenger app.
"""
import uuid
from django.db import models
from main.models import CustomUser


class Conversation(models.Model):
    """
    A conversation model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        """
        String representation of a user's name.
        """
        return f"{self.name}"


class Message(models.Model):
    """
    A message model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="messages_to_me"
    )
    text = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of a conversation, includes members of
        the conversation, a message text, and a timestamp.
        """
        return (f"From {self.from_user} to {self.to_user}: "
                f"{self.text} [{self.timestamp}]")
