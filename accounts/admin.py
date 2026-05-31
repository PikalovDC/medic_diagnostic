from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'phone', 'is_patient', 'is_doctor', 'is_staff')
    list_filter = ('is_patient', 'is_doctor', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone',
                       'birth_date', 'address')
        }),
        ('Медицинская информация', {
            'fields': ('medical_card_number', 'blood_type')
        }),
        ('Роли', {
            'fields': ('is_patient', 'is_doctor')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
