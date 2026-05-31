import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ПОЛНАЯ ПРОВЕРКА ПРОЕКТА")
print("=" * 60)

# 1. Проверка моделей
print("\n1. ПРОВЕРКА МОДЕЛЕЙ:")
try:
    from services.models import ServiceCategory, Service

    print(f"✓ Services: {ServiceCategory.objects.count()} категорий, {Service.objects.count()} услуг")
except Exception as e:
    print(f"✗ Services: {e}")

try:
    from accounts.models import CustomUser

    print(f"✓ Accounts: {CustomUser.objects.count()} пользователей")
except Exception as e:
    print(f"✗ Accounts: {e}")

try:
    from appointments.models import Doctor, Appointment

    print(f"✓ Appointments: {Doctor.objects.count()} врачей, {Appointment.objects.count()} записей")
except Exception as e:
    print(f"✗ Appointments: {e}")

# 2. Проверка шаблонов
print("\n2. ПРОВЕРКА ШАБЛОНОВ:")
template_paths = [
    'templates/base/base.html',
    'templates/services/list.html',
    'templates/services/detail.html',
    'templates/accounts/appointment_history.html',
]

for path in template_paths:
    if os.path.exists(path):
        print(f"✓ {path}")
    else:
        print(f"✗ {path} - не найден")

# 3. Проверка статических файлов
print("\n3. ПРОВЕРКА СТАТИЧЕСКИХ ФАЙЛОВ:")
static_paths = [
    'static/css/style.css',
    'static/js/main.js',
]

for path in static_paths:
    if os.path.exists(path):
        print(f"✓ {path}")
    else:
        print(f"✗ {path} - не найден")

# 4. Проверка URL
print("\n4. ПРОВЕРКА URL:")
try:
    from django.urls import get_resolver

    resolver = get_resolver()
    url_patterns = []


    def list_urls(urlpatterns, base=''):
        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                list_urls(pattern.url_patterns, base + str(pattern.pattern))
            else:
                url_patterns.append(base + str(pattern.pattern))


    list_urls(resolver.url_patterns)
    print(f"✓ Найдено {len(url_patterns)} URL-шаблонов")
except Exception as e:
    print(f"✗ URLs: {e}")

print("\n" + "=" * 60)
print("РЕКОМЕНДАЦИИ:")
print("1. Если нет static/css/style.css - создайте пустой файл")
print("2. Если ошибка в шаблоне - используйте list_simple.html")
print("=" * 60)
