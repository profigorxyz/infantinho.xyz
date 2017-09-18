from django.contrib import admin

# Register your models here.
from .models import Achiev, Area, SubArea, SubSubArea, StudentSysLevel


admin.site.register(Achiev)
admin.site.register(Area)
admin.site.register(SubArea)
admin.site.register(SubSubArea)
admin.site.register(StudentSysLevel)
