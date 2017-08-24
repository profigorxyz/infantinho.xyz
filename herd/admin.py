from django.contrib import admin
from .models import Grade, Student, Teacher, Subject


class StudentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'grade']
    list_display_links = ['user', 'grade']
    list_filter = ['grade']
    search_fields = ['user', 'grade']

    class Meta:
        model = Student


admin.site.register(Grade)
admin.site.register(Student, StudentModelAdmin)
admin.site.register(Teacher)
admin.site.register(Subject)
