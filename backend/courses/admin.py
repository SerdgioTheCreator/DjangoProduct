from django.contrib import admin

from courses.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'title',
        'description', 'price', 'is_active'
    )
    list_filter = ('author', 'price', 'is_active',)
