from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    # Дополнительные поля
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True,
        null=True
    )

    birth_date = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True
    )

    address = models.TextField(
        verbose_name="Адрес",
        blank=True,
        null=True
    )

    # Медицинские поля
    medical_card_number = models.CharField(
        max_length=50,
        verbose_name="Номер медицинской карты",
        blank=True,
        null=True
    )

    blood_type = models.CharField(
        max_length=5,
        verbose_name="Группа крови",
        blank=True,
        null=True
    )

    is_patient = models.BooleanField(
        default=True,
        verbose_name="Является пациентом"
    )

    is_doctor = models.BooleanField(
        default=False,
        verbose_name="Является врачом"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
