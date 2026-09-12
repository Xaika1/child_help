from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('my_sessions/', views.my_sessions, name='my_sessions'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),  # ← ДОБАВЛЕНО
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('login_/', views.login_view, name='login_'),
]