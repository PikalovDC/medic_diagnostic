# check_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import ServiceCategory, Service

print('Проверяем данные в базе...')

# Проверим категории
try:
    cat_count = ServiceCategory.objects.count()
    print(f'Категорий в базе: {cat_count}')

    for cat in ServiceCategory.objects.all():
        print(f'  - {cat.name} (ID: {cat.id})')
        # Проверим, есть ли услуги в категории
        service_count = cat.services.count()
        print(f'    Услуг в категории: {service_count}')

except Exception as e:
    print(f'Ошибка при проверке категорий: {e}')

# Проверим услуги
try:
    service_count = Service.objects.count()
    print(f'\nУслуг в базе: {service_count}')

    for service in Service.objects.all()[:10]:  # первые 10
        category_name = service.category.name if service.category else "Нет категории"
        print(f'  - {service.name} (Категория: {category_name}, Цена: {service.price} руб.)')

except Exception as e:
    print(f'Ошибка при проверке услуг: {e}')
