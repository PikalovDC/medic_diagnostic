from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from appointments.models import Doctor

def home(request):
    """Главная страница"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно отправить email или сохранить в БД
            messages.success(request, 'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.')
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'title': 'Медицинская Диагностика - Главная',
        'services': [
            {'name': 'МРТ', 'icon': 'bi-magnet', 'description': 'Магнитно-резонансная томография всего тела'},
            {'name': 'КТ', 'icon': 'bi-cpu', 'description': 'Компьютерная томография высокой точности'},
            {'name': 'УЗИ', 'icon': 'bi-soundwave', 'description': 'Ультразвуковая диагностика'},
            {'name': 'Анализы', 'icon': 'bi-droplet', 'description': 'Лабораторные исследования'},
        ],
        'form': form
    }
    return render(request, 'main/home.html', context)


def contacts(request):
    """Страница контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Сообщение отправлено! Мы ответим вам в течение 24 часов.')
            return redirect('contacts')
    else:
        form = ContactForm()

    return render(request, 'main/contacts.html', {
        'title': 'Контакты',
        'form': form
    })


def about(request):
    """Страница о компании"""
    doctors = Doctor.objects.filter(is_active=True)

    return render(request, 'main/about.html', {
        'title': 'О компании',
        'doctors': doctors
    })