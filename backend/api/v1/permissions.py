from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsGroupLessonCourseAuthorOrIsAdmin(BasePermission):
    """Админы и авторы курса имеют полный доступ к урокам и группам курса."""

    def has_permission(self, request, view):
        if request.user.is_student:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return obj.course.author == request.user or request.user.is_admin


class IsCourseAuthorOrIsAdmin(BasePermission):
    """Админы и авторы курса имеют полный доступ к курсу."""

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_admin
                or request.method in SAFE_METHODS)
