"""
Views of messenger api.
"""
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from django.db.models import Q
from django.db.utils import DatabaseError
from rest_framework import status
from messenger.api.pagynaters import MessagePagination
from messenger.api.serialisers import ConversationSerializer, MessageSerializer
from messenger.models import Conversation, Message


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    A viewset for viewing and retrieving Conversation objects.
    """
    serializer_class = ConversationSerializer
    # pylint: disable=no-member
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        """
        Return a queryset of conversations that contain
        the current user's ID.
        """
        try:
            # pylint: disable=no-member
            queryset = Conversation.objects.filter(
                name__contains=self.request.user.id
            )
            return queryset
        except DatabaseError as error:
            print(f'Error connecting to the database: {error}')
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response({"error": "Error connecting to the database"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Return the request and current user in the serializer context.
        """
        return {"request": self.request, "user": self.request.user}


class MessageViewSet(ListModelMixin, GenericViewSet):
    """
    A viewset for viewing and retrieving Message objects.
    """
    serializer_class = MessageSerializer
    # pylint: disable=no-member
    queryset = Message.objects.none()
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Return a queryset of conversations that contain the current
        user's ID in their name.
        """
        try:
            conversation_name = self.request.GET.get("conversation")
            queryset = (
                # pylint: disable=no-member
                Message.objects.filter(
                    Q(to_user=self.request.user.id) |
                    Q(from_user=self.request.user.id)
                )
                .filter(conversation__name=conversation_name)
                .order_by("-timestamp")
            )
            return queryset
        except DatabaseError as error:
            print(f'Error connecting to the database: {error}')
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response({"error": "Error connecting to the database"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
