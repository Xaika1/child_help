from django.db import models


class Users(models.Model):
    """Пациенты/Пользователи"""
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login


class Staff(models.Model):
    """Врачи (id, логин, пароль и должность)"""
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, verbose_name='Должность')

    class Meta:
        db_table = 'staff'
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['specialization', 'login']

    def __str__(self):
        return f"{self.login} ({self.specialization})"


class StaffInfo(models.Model):
    """Дополнительная информация о враче"""
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='info')
    education = models.TextField(blank=True, null=True, verbose_name='Образование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'staff_info'
        verbose_name = 'Информация о враче'
        verbose_name_plural = 'Информация о врачах'

    def __str__(self):
        return f"Инфо о {self.staff.login}"


class Sessions(models.Model):
    """Записи на приём (user_id, staff_id, время, комментарий)"""
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='appointments', verbose_name='Пользователь')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='appointments', verbose_name='Врач')
    appointment_time = models.DateTimeField(verbose_name='Время приёма')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        db_table = 'sessions'
        verbose_name = 'Запись на приём'
        verbose_name_plural = 'Записи на приём'
        ordering = ['appointment_time']

    def __str__(self):
        return f"{self.user.login} → {self.staff.login} ({self.appointment_time})"