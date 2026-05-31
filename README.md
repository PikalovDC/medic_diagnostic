# 🏥 Медицинский Диагностический Центр

Веб-приложение для компании медицинской диагностики на Django + Bootstrap.

## 🚀 Особенности

- **Современный адаптивный дизайн** на Bootstrap 5
- **Полнофункциональная система записи** на прием
- **Личные кабинеты** для пациентов и врачей
- **Административная панель** для управления контентом
- **REST API** для медицинских услуг

## 📋 Функционал

### Для пациентов:
- 📝 Регистрация и авторизация
- 📅 Запись на прием онлайн
- 📋 Просмотр истории записей
- 💬 Обратная связь с клиникой

### Для администраторов:
- 👥 Управление пользователями
- 🏥 Управление услугами и ценами
- 👨‍⚕️ Управление врачами
- 📊 Просмотр статистики записей

## 🛠 Технологии

- **Backend:** Django 4.2, Django REST Framework
- **Frontend:** Bootstrap 5, JavaScript
- **База данных:** SQLite (разработка), PostgreSQL (продакшен)
- **Контейнеризация:** Docker, Docker Compose

## ⚡ Быстрый старт

1. Установка (без Docker)

- **Клонирование репозитория**

git clone <ваш-репозиторий>

cd medical_diagnostic

- **Создание виртуального окружения**

python -m venv venv

source venv/bin/activate  # Linux/Mac

- **или**

venv\Scripts\activate     # Windows

- **Установка зависимостей**

pip install -r requirements.txt

- **Настройка базы данных**

python manage.py migrate

python manage.py createsuperuser

python create_test_data.py

- **Запуск сервера**

python manage.py runserver

2. Запуск с Docker

- **Сборка и запуск**

docker-compose -f docker-compose-simple.yml up --build

- **Или для продакшена**

docker-compose up --build


## 📁 Структура проекта

medical_diagnostic/
- ├── accounts/           # Пользователи и аутентификация
- ├── appointments/       # Записи на прием
- ├── services/          # Медицинские услуги
- ├── main/             # Основные страницы
- ├── config/           # Настройки Django
- ├── templates/        # HTML шаблоны
- ├── static/           # Статические файлы
- ├── media/            # Загружаемые файлы
- └── manage.py         # Точка входа Django

## 🔧 Настройка окружения

**Создайте файл .env в корне проекта:**

DEBUG=True

SECRET_KEY=ваш-секретный-ключ

ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=sqlite:///db.sqlite3

## 👥 Тестовые пользователи
**После запуска create_test_data.py создаются:**
- Администратор: admin / admin123
- Врачи: dr_ivanov / doctor123, dr_petrova / doctor123
- Пациент: testuser / test123

## 📞 Контакты и поддержка
- Email: support@meddiagnostic.ru
- Сайт: http://meddiagnostic.ru
- Телефон: +7 (495) 123-45-67

## 📄 Лицензия
- MIT License

## 🎯 Демонстрация
- Главная страница: /
- Услуги: /services/
- Запись на прием: /appointments/create/
- Админ-панель: /admin/
-API: /services/api/