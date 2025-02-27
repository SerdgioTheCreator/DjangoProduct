from django.urls import include, path, re_path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
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
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
