from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Lesson, Well


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class WellSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Well
        fields = "__all__"


class WellDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    def get_lessons_count(self, object):
        return object.lesson_set.count()

    class Meta:
        model = Well
        fields = ("name", "description", "lessons_count", "lessons")
