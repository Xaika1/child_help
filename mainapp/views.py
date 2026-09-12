from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages  # <-- ДОБАВЛЕНО
from django.shortcuts import render, redirect, get_object_or_404  # <-- get_object_or_404 тоже здесь
from .forms import RegisterForm
from .models import Staff, Users, Sessions


"""Рендер первой страницы"""
@login_required(login_url='/login/')
def index(request):
    staff_list = Staff.objects.select_related('info').order_by('specialization', 'login')
    return render(request, 'main/main.html', {'staff_list': staff_list})


"""Обработка формы записи на приём"""
@login_required(login_url='/login/')
def booking(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        comment = request.POST.get('comment', '')

        try:
            staff = Staff.objects.get(id=doctor_id)
            # Получаем текущего пользователя (стандартный User Django)
            user_obj = request.user
            # Находим соответствующую запись в Users по логину
            try:
                custom_user = Users.objects.get(login=user_obj.username)
            except Users.DoesNotExist:
                # Если записи в Users нет — создаём
                custom_user = Users.objects.create(
                    login=user_obj.username,
                    password='auto'  # пароль уже хеширован в User
                )

            appointment_time = f"{date} {time}"
            Sessions.objects.create(
                user=custom_user,
                staff=staff,
                appointment_time=appointment_time,
                comment=comment
            )
            messages.success(request, f'Вы записаны к {staff.login} на {date} в {time}')
        except Staff.DoesNotExist:
            messages.error(request, 'Врач не найден')
        except Exception as e:
            messages.error(request, f'Ошибка при записи: {e}')

        return redirect('index')

    return redirect('index')
@login_required(login_url='/login_/')
def my_sessions(request):
    

    """Выводит список записей текущего пользователя"""
    
    # 1. Находим нашего пользователя в таблице Users по логину авторизованного аккаунта Django
    try:
        custom_user = Users.objects.get(login=request.user.username)
    except Users.DoesNotExist:
        # Если записи еще нет (например, пользователь только что зарегистрировался), создаем её
        custom_user = Users.objects.create(login=request.user.username, password='auto')

    # 2. Получаем все записи этого пользователя
    # select_related('staff') сразу подгружает данные врача, чтобы избежать лишних запросов к БД
    # order_by('appointment_time') сортирует записи по времени (от ближайших к дальним)
    appointments = Sessions.objects.filter(user=custom_user).select_related('staff').order_by('appointment_time')

    return render(request, 'main/my_sessions.html', {
        'appointments': appointments
    })

@login_required(login_url='/login_/')
def cancel_appointment(request, appointment_id):
    """Отмена записи на приём"""
    if request.method == 'POST':
        appointment = get_object_or_404(Sessions, id=appointment_id)

        # Проверяем, что запись принадлежит текущему пользователю
        try:
            custom_user = Users.objects.get(login=request.user.username)
        except Users.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
            return redirect('my_sessions')

        if appointment.user != custom_user:
            messages.error(request, 'Вы не можете отменить эту запись')
            return redirect('my_sessions')

        # Удаляем запись
        appointment.delete()
        messages.success(request, 'Запись успешно отменена')

    return redirect('my_sessions')
"""Выход из аккаунта"""
@login_required(login_url='/login/')
def logout_view(request):
    auth_logout(request)
    return redirect('login')


"""Вход в аккаунт"""
def login_view(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'registration/login.html')


"""Регистрация"""
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/reg.html', {"form": form})