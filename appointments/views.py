from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, Doctor
from services.models import Service
from accounts.models import CustomUser


@login_required
def appointment_list(request):
    """Список записей пользователя"""
    try:
        appointments = Appointment.objects.filter(
            patient=request.user
        ).order_by('-appointment_date', '-appointment_time')

        # Статистика
        pending = appointments.filter(status='pending').count()
        confirmed = appointments.filter(status='confirmed').count()
        completed = appointments.filter(status='completed').count()

        context = {
            'title': 'Мои записи',
            'appointments': appointments,
            'pending_count': pending,
            'confirmed_count': confirmed,
            'completed_count': completed,
            'today': timezone.now().date(),
        }
        return render(request, 'appointments/list.html', context)

    except Exception as e:
        print(f"[ERROR] appointment_list: {e}")
        # Временное решение - простая страница
        return render(request, 'appointments/simple_list.html', {
            'title': 'Мои записи',
            'appointments': [],
        })


@login_required
def create_appointment(request):
    """Создание новой записи на прием"""
    try:
        services = Service.objects.filter(is_active=True)
        doctors = Doctor.objects.filter(is_active=True)

        selected_service_id = request.GET.get('service')

        if request.method == 'POST':
            # Упрощенная обработка для теста
            service_id = request.POST.get('service')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

            if service_id and appointment_date and appointment_time:
                service = Service.objects.get(id=service_id)

                appointment = Appointment.objects.create(
                    patient=request.user,
                    service=service,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status='pending',
                    notes=request.POST.get('notes', '')
                )

                messages.success(request,
                                 f'Запись на {appointment.service.name} создана! ' +
                                 'Мы свяжемся с вами для подтверждения.')
                return redirect('appointments:list')
            else:
                messages.error(request, 'Заполните все обязательные поля')

        context = {
            'title': 'Запись на прием',
            'services': services,
            'doctors': doctors,
            'selected_service_id': selected_service_id,
            'today': timezone.now().date().isoformat(),
            'min_date': (timezone.now().date()).isoformat(),
        }
        return render(request, 'appointments/create.html', context)

    except Exception as e:
        print(f"[ERROR] create_appointment: {e}")
        messages.error(request, f'Ошибка при создании записи: {str(e)}')
        return redirect('appointments:list')


@login_required
def appointment_detail(request, pk):
    """Детали записи"""
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)

    context = {
        'title': f'Запись #{appointment.id}',
        'appointment': appointment,
    }
    return render(request, 'appointments/detail.html', context)


@login_required
def cancel_appointment(request, pk):
    """Отмена записи"""
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        patient=request.user,
        status__in=['pending', 'confirmed']
    )

    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Запись успешно отменена.')
        return redirect('appointments:list')

    return render(request, 'appointments/cancel.html', {
        'appointment': appointment
    })
