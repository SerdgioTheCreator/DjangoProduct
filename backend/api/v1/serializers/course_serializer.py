from rest_framework import serializers

from core.constants import GROUPS_LIMIT, HUNDRED, ONE, USERS_LIMIT, ZERO
from courses.models import Course, Group, Lesson
from users.models import CustomUser


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


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    course = serializers.StringRelatedField(source='course.title', read_only=True)
    users = serializers.StringRelatedField(many=True, read_only=True)

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

    author = serializers.StringRelatedField(read_only=True)
    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум USERS_LIMIT чел."""
        return round(
            obj.students_count / (GROUPS_LIMIT * USERS_LIMIT) * HUNDRED,
            ONE
        )

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_users = CustomUser.objects.count()
        return round(obj.students_count / total_users * HUNDRED) if total_users > ZERO else ZERO

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
