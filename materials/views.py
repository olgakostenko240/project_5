from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Lesson, Well, Subscription
from materials.serializers import LessonSerializer, WellSerializer, WellDetailSerializer, SubscriptionSerializer
from materials.paginations import CustomPagination
from users.permissions import IsModer, IsOwner


class WellViewSet(ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WellDetailSerializer
        return WellSerializer

    def perform_create(self, serializer):
        well = serializer.save()
        well.owner = self.request.user
        well.save()

    def get_permissions(self):
        if self.action in ["retrieve", "update"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)


class SubscriptionCreateApiView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        well_id = self.request.data.get('well')
        well_item = get_object_or_404(Well, pk=well_id)
        subs_item = Subscription.objects.filter(user=user, well=well_item)

        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, well=well_item, sign_of_subscription=True)  # Создаем подписку
            message = 'подписка добавлена'
        return Response({"message": message})
