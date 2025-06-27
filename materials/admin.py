from django.contrib import admin

from materials.models import Well, Lesson


@admin.register(Well)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview', 'description', 'link_to_video', 'well')
    list_filter = ('name', 'well',)
    search_fields = ('name', 'well',)
