from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from api.v1.permissions import (IsCourseAuthorOrIsAdmin,
                                IsGroupLessonCourseAuthorOrIsAdmin)
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from courses.models import Course


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsAuthenticated, IsGroupLessonCourseAuthorOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        if course.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('Вы не можете добавлять уроки в чужой курс.')
        return serializer.save(course=course)

    def perform_update(self, serializer):
        lesson = self.get_object()
        if lesson.course.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('Вы не можете изменять уроки в чужом курсе.')

        updated_course = serializer.validated_data.get('course', lesson.course)
        if updated_course != lesson.course:
            raise PermissionDenied('Нельзя менять курс у урока.')

        serializer.save()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (IsAuthenticated, IsGroupLessonCourseAuthorOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        if course.author != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied('Вы не можете добавлять группы в чужой курс.')
        serializer.save(course=course)

    def perform_update(self, serializer):
        group = self.get_object()
        if group.course.author != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied('Вы не можете изменять группы в чужом курсе.')

        updated_course = serializer.validated_data.get("course", group.course)
        if updated_course != group.course:
            raise PermissionDenied('Нельзя менять курс у группы.')

        serializer.save()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

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
