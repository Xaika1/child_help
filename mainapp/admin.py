from django.contrib import admin
from .models import Users, Staff, StaffInfo, Sessions


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'login')
    search_fields = ('login',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'specialization')
    search_fields = ('login',)
    list_filter = ('specialization',)


@admin.register(StaffInfo)
class StaffInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'education')
    search_fields = ('staff__login',)


@admin.register(Sessions)
class SessionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'staff', 'appointment_time', 'comment')
    list_filter = ('staff', 'appointment_time')
    search_fields = ('user__login', 'staff__login')