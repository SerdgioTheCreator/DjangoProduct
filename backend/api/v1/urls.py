from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views.course_view import CourseViewSet, GroupViewSet, LessonViewSet
from api.v1.views.user_view import CustomUserViewSet, PurchaseViewSet


router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('purchases', PurchaseViewSet, basename='purchases')
router.register('courses', CourseViewSet, basename='courses')
router.register(r'courses/(?P<course_id>\d+)/groups', GroupViewSet, basename='groups')
router.register(r'courses/(?P<course_id>\d+)/lessons', LessonViewSet, basename='lessons')
urlpatterns = [
    path('', include(router.urls)),
]
