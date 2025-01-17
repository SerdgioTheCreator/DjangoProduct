from django.conf import settings
from django.contrib import admin
from django.urls import path

from debug_toolbar.toolbar import debug_toolbar_urls


if settings.TESTING:
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
else:
    urlpatterns = [
                      path('admin/', admin.site.urls),
                  ] + debug_toolbar_urls()
