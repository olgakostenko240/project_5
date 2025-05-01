from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from materials.models import Lesson, Well
from materials.serializers import LessonSerializer, WellSerializer, WellDetailSerializer
from users.permissions import IsModer, IsOwner


class WellViewSet(ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer

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
