from django.contrib import admin
from courses.models import Subject, Course, Module

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'overview']
    inlines = [ModuleInline]
