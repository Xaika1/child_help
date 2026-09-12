from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    """Профиль врача (расширение стандартного User)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255, default='Врач')
    
    class Meta:
        db_table = 'staff'  # ← Правильное имя таблицы!
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.user.username


class StaffInfo(models.Model):
    """Дополнительная информация о враче"""
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='info')
    education = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    work_history = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'staff_info'
        verbose_name = 'Информация о враче'
        verbose_name_plural = 'Информация о врачах'

    def __str__(self):
        return f"Инфо о {self.staff.user.username}"


class Sessions(models.Model):
    """Сессии пользователей"""
    token = models.CharField(max_length=255, unique=True)
    owner_id = models.IntegerField()
    owner_type = models.CharField(max_length=10, choices=[
        ('user', 'Пользователь'),
        ('staff', 'Врач'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'sessions'
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def __str__(self):
        return f"Сессия {self.owner_type} #{self.owner_id}"