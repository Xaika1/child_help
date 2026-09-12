from django.contrib import admin
from .models import Staff, StaffInfo, Sessions


# Стало:
from .models import Staff, StaffInfo, Sessions

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'specialization')

@admin.register(StaffInfo)
class StaffInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'education')

@admin.register(Sessions)
class SessionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'owner_type', 'owner_id')