from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Progress)
admin.site.register(Volunteer)
admin.site.register(Task)
admin.register(Slot)

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_id', '__str__')
