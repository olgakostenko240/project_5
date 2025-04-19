from rest_framework.serializers import ModelSerializer

from materials.models import Lesson, Well


class WellSerializer(ModelSerializer):
    class Meta:
        model = Well
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
