from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.permissions import (IsCourseAuthorOrIsAdmin,
                                IsLessonOrGroupAccessible)
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from courses.models import Course, Group, Lesson
from users.models import Purchase


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsAuthenticated, IsLessonOrGroupAccessible,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def get_queryset(self):
        return Lesson.objects.select_related(
            'course'
        ).filter(
            course_id=self.kwargs.get('course_id')
        )

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return serializer.save(course=course)


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (IsAuthenticated, IsLessonOrGroupAccessible,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def get_queryset(self):
        return Group.objects.select_related(
            'course'
        ).filter(
            course_id=self.kwargs.get('course_id')
        )

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы."""

    permission_classes = (IsAuthenticated, IsCourseAuthorOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    def get_queryset(self):
        queryset = Course.objects.annotate(
            students_count=Count('purchases', distinct=True),
            lessons_count=Count('lessons')
        ).select_related('author').prefetch_related('lessons')
        if self.request.user.is_admin:
            return queryset
        return queryset.filter(is_active=True)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def pay(self, request, pk=None):
        """Покупка доступа к курсу."""
        course = self.get_object()
        Purchase.objects.create_purchase(user=request.user, course=course)
        return Response({'detail': 'Покупка доступа к курсу прошла успешно.'}, status=status.HTTP_201_CREATED)
