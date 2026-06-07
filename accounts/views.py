from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from appointments.models import Appointment


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


@login_required
def profile_view(request):
    """Профиль пользователя"""
    user_appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-appointment_date')

    context = {
        'title': 'Мой профиль',
        'appointments': user_appointments,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def appointment_history(request):
    """История записей"""
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-appointment_date', '-appointment_time')

    context = {
        'title': 'Мои записи',
        'appointments': appointments,
    }
    return render(request, 'accounts/appointment_history.html', context)
