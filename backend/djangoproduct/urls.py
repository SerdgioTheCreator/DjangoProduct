from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]

if not settings.TESTING and settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
