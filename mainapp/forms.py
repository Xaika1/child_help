from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Users  # Импортируем конкретно нашу модель Users


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    
    class Meta:
        model = User  
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Логин",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
    
    def save(self, commit=True):
        # 1. Создаём стандартного пользователя Django (нужен для системы авторизации)
        user = super().save(commit=False) 
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # 2. Создаём запись в нашей кастомной таблице Users (нужна для логики записей)
            Users.objects.create(
                login=user.username,
                password='auto'  # Реальный пароль уже безопасно хранится в стандартной таблице User
            )
        
        return user