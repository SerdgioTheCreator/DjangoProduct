from django.contrib import admin

from courses.models import Course, Group, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'title',
        'description', 'price', 'is_active'
    )
    list_filter = ('author', 'is_active',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'link')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')
