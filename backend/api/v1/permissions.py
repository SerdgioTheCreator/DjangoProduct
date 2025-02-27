from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, BasePermission

from courses.models import Course
from users.models import Purchase


class IsLessonOrGroupAccessible(BasePermission):
    """
    Студенты: имеют доступ к группам и урокам только купленных курсов.
    Преподаватели: имеют доступ к группам и урокам только тех курсов, авторами которых являются.
    Админ: имеет полный доступ.
    """

    def has_permission(self, request, view):
        user = request.user
        course = get_object_or_404(
            Course.objects.select_related('author'),
            id=view.kwargs.get("course_id")
        )

        if user == course.author or user.is_admin:
            return True

        return request.method in SAFE_METHODS and Purchase.objects.filter(course_id=course.id,
                                                                          user_id=user.id).exists()

    def has_object_permission(self, request, view, obj):
        return (
                obj.course.author == request.user
                or request.user.is_admin
                or (request.method in SAFE_METHODS and Purchase.objects.filter(course_id=obj.course.id,
                                                                               user_id=request.user.id).exists())
        )


class IsCourseAuthorOrIsAdmin(BasePermission):
    """Админы и авторы курса имеют полный доступ к курсу."""

    def has_permission(self, request, view):
        if request.user.is_student:
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_admin
                or request.method in SAFE_METHODS)
