# create_test_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import ServiceCategory, Service
from accounts.models import CustomUser  # Импортируем CustomUser
from appointments.models import Doctor  # Импортируем Doctor

print('Создаем категории услуг...')

# 1. Создаем категории
categories = [
    {'name': 'Аппаратная диагностика', 'icon': 'bi-magnet',
     'description': 'Современные аппаратные методы исследования'},
    {'name': 'Лабораторные исследования', 'icon': 'bi-droplet',
     'description': 'Анализы крови, мочи и другие лабораторные тесты'},
    {'name': 'Ультразвуковая диагностика', 'icon': 'bi-soundwave',
     'description': 'УЗИ различных органов и систем'},
    {'name': 'Функциональная диагностика', 'icon': 'bi-activity',
     'description': 'ЭКГ, спирометрия и другие исследования'},
]

created_cats = []
for i, cat_data in enumerate(categories, 1):
    cat, created = ServiceCategory.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'icon': cat_data['icon'],
            'description': cat_data['description']
        }
    )
    created_cats.append(cat)
    print(f'{i}. {cat.name}')

print('\nСоздаем услуги...')

# 2. Создаем услуги
services_data = [
    # Аппаратная диагностика
    {'name': 'МРТ головного мозга', 'category': 0, 'price': 5200, 'duration': 60,
     'description': 'Магнитно-резонансная томография головного мозга'},
    {'name': 'КТ грудной клетки', 'category': 0, 'price': 4800, 'duration': 45,
     'description': 'Компьютерная томография органов грудной клетки'},
    {'name': 'Маммография', 'category': 0, 'price': 3500, 'duration': 30,
     'description': 'Рентгенологическое исследование молочных желез'},

    # Лабораторные исследования
    {'name': 'Общий анализ крови', 'category': 1, 'price': 850, 'duration': 15,
     'description': 'Развернутый клинический анализ крови'},
    {'name': 'Биохимический анализ крови', 'category': 1, 'price': 2200, 'duration': 20,
     'description': 'Комплексный биохимический анализ'},
    {'name': 'Анализ мочи общий', 'category': 1, 'price': 650, 'duration': 10,
     'description': 'Общий клинический анализ мочи'},

    # Ультразвуковая диагностика
    {'name': 'УЗИ брюшной полости', 'category': 2, 'price': 2700, 'duration': 40,
     'description': 'Ультразвуковое исследование органов брюшной полости'},
    {'name': 'УЗИ щитовидной железы', 'category': 2, 'price': 1900, 'duration': 30,
     'description': 'Ультразвуковое исследование щитовидной железы'},
    {'name': 'УЗИ молочных желез', 'category': 2, 'price': 2300, 'duration': 35,
     'description': 'Ультразвуковое исследование молочных желез'},

    # Функциональная диагностика
    {'name': 'ЭКГ (электрокардиограмма)', 'category': 3, 'price': 1200, 'duration': 20,
     'description': 'Электрокардиографическое исследование сердца'},
    {'name': 'Суточное мониторирование ЭКГ', 'category': 3, 'price': 4500, 'duration': 1440,
     'description': 'Холтеровское мониторирование сердечной деятельности'},
    {'name': 'Спирометрия', 'category': 3, 'price': 1800, 'duration': 30,
     'description': 'Исследование функции внешнего дыхания'},
]

for i, service_data in enumerate(services_data, 1):
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults={
            'category': created_cats[service_data['category']],
            'price': service_data['price'],
            'duration': service_data['duration'],
            'description': service_data['description'],
            'full_description': f'Полное описание услуги "{service_data["name"]}". Современное оборудование, квалифицированные специалисты, точные результаты.',
            'preparation': 'Специальной подготовки не требуется' if service_data[
                                                                        'category'] != 1 else 'Сдача анализов проводится натощак',
            'contraindications': 'Индивидуальные противопоказания уточняйте у врача',
            'is_active': True
        }
    )
    print(f'{i}. {service.name} - {service.price} руб.')

print(f'\n✅ Услуги созданы!')
print(f'   - Категорий: {ServiceCategory.objects.count()}')
print(f'   - Услуг: {Service.objects.count()}')
print(f'   - Активных услуг: {Service.objects.filter(is_active=True).count()}')

# 3. Создаем врачей
print('\n' + '=' * 50)
print('Создаем врачей...')

# Сначала проверяем, есть ли уже суперпользователь
try:
    admin_user = CustomUser.objects.get(username='admin')
    print('✓ Суперпользователь admin уже существует')
except CustomUser.DoesNotExist:
    print('✗ Суперпользователь admin не найден')

# Данные врачей
doctors_data = [
    {
        'username': 'dr_ivanov',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'email': 'ivanov@meddiagnostic.ru',
        'specialty': 'Терапевт',
        'education': 'МГМУ им. Сеченова, высшая категория',
        'experience': 15,
    },
    {
        'username': 'dr_petrova',
        'first_name': 'Мария',
        'last_name': 'Петрова',
        'email': 'petrova@meddiagnostic.ru',
        'specialty': 'Кардиолог',
        'education': 'РНИМУ им. Пирогова, кандидат медицинских наук',
        'experience': 12,
    },
    {
        'username': 'dr_sidorov',
        'first_name': 'Алексей',
        'last_name': 'Сидоров',
        'email': 'sidorov@meddiagnostic.ru',
        'specialty': 'Невролог',
        'education': 'СПбГМУ им. Павлова, доктор медицинских наук',
        'experience': 10,
    },
    {
        'username': 'dr_smirnova',
        'first_name': 'Елена',
        'last_name': 'Смирнова',
        'email': 'smirnova@meddiagnostic.ru',
        'specialty': 'УЗИ-специалист',
        'education': 'КГМУ, высшая категория',
        'experience': 8,
    },
]

created_doctors = []
for i, doc_data in enumerate(doctors_data, 1):
    # Проверяем, существует ли пользователь
    try:
        user = CustomUser.objects.get(username=doc_data['username'])
        print(f'{i}. Пользователь {doc_data["username"]} уже существует')
    except CustomUser.DoesNotExist:
        # Создаем нового пользователя
        user = CustomUser.objects.create_user(
            username=doc_data['username'],
            first_name=doc_data['first_name'],
            last_name=doc_data['last_name'],
            email=doc_data['email'],
            password='doctor123',  # Стандартный пароль
            is_doctor=True,
            is_patient=False,
        )
        print(f'{i}. Создан пользователь: {doc_data["first_name"]} {doc_data["last_name"]}')

    # Создаем или обновляем профиль врача
    doctor, created = Doctor.objects.get_or_create(
        user=user,
        defaults={
            'specialty': doc_data['specialty'],
            'education': doc_data['education'],
            'experience': doc_data['experience'],
            'license_number': f'MED-LIC-{1000 + i}',
            'is_active': True,
        }
    )

    if created:
        created_doctors.append(doctor)
        print(f'   ✓ Создан врач: {doc_data["specialty"]}')
    else:
        print(f'   ✓ Врач уже существует: {doc_data["specialty"]}')

print('\n' + '=' * 50)
print('✅ ВСЕГО СОЗДАНО:')
print(f'   - Категорий услуг: {ServiceCategory.objects.count()}')
print(f'   - Медицинских услуг: {Service.objects.count()}')
print(f'   - Врачей: {Doctor.objects.count()}')
print(f'   - Пользователей: {CustomUser.objects.count()}')

# 4. Создаем тестовые записи на прием (опционально)
print('\n' + '=' * 50)
print('Создаем тестовые записи на прием...')

# Получаем обычного пользователя для теста
try:
    test_patient = CustomUser.objects.get(username='testuser')
except CustomUser.DoesNotExist:
    # Создаем тестового пациента если нет
    test_patient = CustomUser.objects.create_user(
        username='testuser',
        first_name='Тестовый',
        last_name='Пациент',
        email='test@meddiagnostic.ru',
        password='test123',
        is_patient=True,
        is_doctor=False,
    )
    print('✓ Создан тестовый пациент: testuser/test123')

# Создаем несколько тестовых записей
from appointments.models import Appointment
from datetime import date, timedelta
import random

# Очищаем старые тестовые записи (опционально)
Appointment.objects.filter(patient=test_patient).delete()

# Создаем новые записи
test_services = Service.objects.filter(is_active=True)[:3]

for i, service in enumerate(test_services, 1):
    appointment_date = date.today() + timedelta(days=i + 5)
    appointment_time = f"{9 + i}:00"

    # Выбираем случайного врача или None
    doctor = random.choice([None] + list(Doctor.objects.filter(is_active=True)[:2]))

    appointment = Appointment.objects.create(
        patient=test_patient,
        doctor=doctor,
        service=service,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status=random.choice(['pending', 'confirmed', 'completed']),
        notes=f'Тестовая запись #{i}',
    )

    status_display = dict(Appointment.STATUS_CHOICES)[appointment.status]
    doctor_name = doctor.user.get_full_name() if doctor else "Любой врач"

    print(f'{i}. Запись создана: {service.name} - {appointment_date} {appointment_time} ({status_display})')

print('\n' + '=' * 50)
print('🎉 ВСЕ ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ УСПЕШНО!')
print('\nДоступы для тестирования:')
print('1. Администратор: admin / ваш_пароль')
print('2. Врачи: dr_ivanov / doctor123, dr_petrova / doctor123, и т.д.')
print('3. Тестовый пациент: testuser / test123')
print('\nЗапустите сервер: python manage.py runserver')
