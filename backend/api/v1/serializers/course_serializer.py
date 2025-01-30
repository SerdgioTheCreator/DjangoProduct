from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.constants import GROUPS_LIMIT, HUNDRED, ONE, USERS_LIMIT
from courses.models import Course, Group, Lesson
from users.models import CustomUser, Purchase

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'id',
            'course',
            'title',
            'link',
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'link'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'id'
            'email',
            'username',
            'first_name',
            'last_name',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'course',
            'users',
            'title',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return Purchase.objects.filter(course=obj.id).count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел."""
        return round(
            obj.purchases.count() / (GROUPS_LIMIT * USERS_LIMIT) * HUNDRED,
            ONE
        )

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_users = CustomUser.objects.count()
        if total_users == 0:
            return 0

        purchases_count = Purchase.objects.filter(course=obj).count()
        return round(purchases_count / total_users * HUNDRED)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'description',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
            'is_active'
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'description',
            'price',
            'is_active',
        )
