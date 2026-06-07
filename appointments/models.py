from django.db import models
from django.conf import settings
from services.models import Service


class Doctor(models.Model):
    """Модель врача"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name="Пользователь"
    )

    specialty = models.CharField(
        max_length=100,
        verbose_name="Специальность"
    )

    education = models.TextField(
        verbose_name="Образование",
        blank=True,
        null=True
    )

    experience = models.IntegerField(
        verbose_name="Стаж (лет)"
    )

    license_number = models.CharField(
        max_length=50,
        verbose_name="Номер лицензии",
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='doctors/',
        verbose_name="Фото",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Работает"
    )

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ['-experience']

    def __str__(self):
        return f"Доктор {self.user.get_full_name()} ({self.specialty})"


class Appointment(models.Model):
    """Модель записи на прием"""

    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
        ('no_show', 'Не явился'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Пациент",
        limit_choices_to={'is_patient': True}
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Врач",
        blank=True,
        null=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Услуга"
    )

    appointment_date = models.DateField(
        verbose_name="Дата приема"
    )

    appointment_time = models.TimeField(
        verbose_name="Время приема"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    notes = models.TextField(
        verbose_name="Примечания",
        blank=True,
        null=True
    )

    diagnosis = models.TextField(
        verbose_name="Диагноз",
        blank=True,
        null=True
    )

    prescription = models.TextField(
        verbose_name="Назначения",
        blank=True,
        null=True
    )

    results_file = models.FileField(
        upload_to='results/',
        verbose_name="Файл с результатами",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ['-appointment_date', 'appointment_time']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.service.name} ({self.appointment_date})"
