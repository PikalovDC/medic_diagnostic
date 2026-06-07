from django.contrib import admin
from .models import Doctor, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialty')
    list_editable = ('is_active',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__username', 'service__name', 'doctor__user__last_name')
    list_editable = ('status',)
    date_hierarchy = 'appointment_date'
    raw_id_fields = ('patient', 'doctor')