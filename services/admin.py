from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    list_per_page = 20
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое создание slug

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'full_description')
        }),
        ('Детали', {
            'fields': ('price', 'duration', 'image')
        }),
        ('Дополнительно', {
            'fields': ('preparation', 'contraindications', 'is_active')
        }),
    )