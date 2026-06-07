from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    """Категория медицинских услуг"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, default="bi-heart",
                            verbose_name="Иконка Bootstrap",
                            help_text="Например: bi-heart, bi-activity, bi-eyedropper")

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Медицинская услуга"""
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL")
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,
                                 related_name='services', verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    full_description = models.TextField(blank=True, verbose_name="Полное описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность (мин)")
    preparation = models.TextField(blank=True, verbose_name="Подготовка к процедуре")
    contraindications = models.TextField(blank=True, verbose_name="Противопоказания")
    image = models.ImageField(upload_to='services/', blank=True, null=True,
                              verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        # Если slug пустой или None
        if not self.slug or self.slug.strip() == '':
            base_slug = slugify(self.name)

            # Проверяем уникальность
            if Service.objects.filter(slug=base_slug).exclude(id=self.id).exists():
                counter = 1
                while Service.objects.filter(slug=f"{base_slug}-{counter}").exists():
                    counter += 1
                self.slug = f"{base_slug}-{counter}"
            else:
                self.slug = base_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.price} руб."
