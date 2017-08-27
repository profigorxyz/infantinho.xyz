from django.contrib import admin
from .models import Grade, Student, Teacher, Subject


<<<<<<< HEAD
class StudentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'grade']
    list_display_links = ['user', 'grade']
    list_filter = ['grade']
    search_fields = ['user', 'grade']

    class Meta:
        model = Student


admin.site.register(Grade)
admin.site.register(Student, StudentModelAdmin)
=======
admin.site.register(Grade)
admin.site.register(Student)
>>>>>>> 334c8eba6362ccffb8257e3a2268669aa495068e
admin.site.register(Teacher)
admin.site.register(Subject)
