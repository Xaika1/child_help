from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

"""Рендер первой страницы"""
@login_required(login_url='/login')
def index(request):
    staff_list = Staff.objects.select_related('info').order_by('specialization', 'login')
    return render(request, 'main/main.html', {'staff_list': staff_list})
@login_required(login_url='/login')
def booking(request):
    pass

"""Выход из аккаунта"""
@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/sign-up')
def login(request):
    login(request, request.user)
    return redirect('/')

"""Регистрация"""
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/reg.html', {"form": form})


