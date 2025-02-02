from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.v1.permissions import (IsCourseAuthorOrIsAdmin,
                                IsLessonOrGroupAccessible)
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from courses.models import Course
from users.models import Purchase


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsAuthenticated, IsLessonOrGroupAccessible,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()

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
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()

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
        if self.request.user.is_admin:
            return Course.objects.all()
        else:
            return Course.objects.filter(is_active=True)

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
