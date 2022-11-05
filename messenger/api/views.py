from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from messenger.api.pagynaters import MessagePagination
from main.models import CustomUser
from messenger.api.serialisers import ConversationSerializer, CustomUserSerializer, MessageSerializer
from messenger.models import Conversation, Message



class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.id
        )
        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}


class CustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    # queryset = CustomUser.objects.all()
    # lookup_field = "username"

    def get_queryset(self):
        return [self.request.user]

    @action(detail=False)
    def all(self, request):
        serializer = CustomUserSerializer(
            CustomUser.objects.all(), many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_name = self.request.GET.get("conversation")
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.id,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset