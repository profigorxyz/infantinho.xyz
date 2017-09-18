from django.contrib import admin
from .models import PresRec


class PresenceModelAdmin(admin.ModelAdmin):
    """docstring for PresenceModelAdmin"""
    list_display = ['subject', 'date', 'student', 'is_absent']
    list_display_links = ['subject', 'date', 'student']
    list_filter = ['subject', 'date', 'student']
    search_fields = ['subject', 'date', 'student']

    class Meta:
        model = PresRec


admin.site.register(PresRec, PresenceModelAdmin)
