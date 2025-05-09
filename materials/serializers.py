from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Lesson, Well, Subscription
from materials.validators import YouTubeValidator



class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeValidator(field="url_video")]


class WellSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Well
        fields = "__all__"


class WellDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    subscription = SerializerMethodField()

    def get_lessons_count(self, well):
        return Lesson.objects.filter(well=well).count()

    def get_subscription(self, well):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user).filter(well=well).exists()

    class Meta:
        model = Well
        fields = ("name", "description", "lessons_count", "lessons", "subscription")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("sign_of_subscription",)
