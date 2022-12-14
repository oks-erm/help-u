from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
# from rest_framework.decorators import action
# from rest_framework import status
# from rest_framework.response import Response
from django.db.models import Q
from messenger.api.pagynaters import MessagePagination
# from main.models import CustomUser
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
        # pylint: disable=no-member
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.id
        )
        return queryset

    def get_serializer_context(self):
        """
        Return the request and current user in the serializer context.
        """
        return {"request": self.request, "user": self.request.user}


# Meant for an extended version of the messenger when you will
# need a list of users.

# class CustomUserViewSet(ModelViewSet):
#     serializer_class = CustomUserSerializer

#     def get_queryset(self):
#         return [self.request.user]

#     @action(detail=False)
#     def all(self, request):
#         serializer = CustomUserSerializer(
#             CustomUser.objects.all(), many=True, context={"request": request}
#         )
#         return Response(status=status.HTTP_200_OK, data=serializer.data)


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
