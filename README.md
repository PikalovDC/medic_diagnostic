# 🏥 Медицинский Диагностический Центр

Веб-приложение для компании медицинской диагностики на Django + Bootstrap.

## 🚀 Особенности

- Современный адаптивный дизайн (светло-зеленая тема)
- Полнофункциональная система записи на прием
- Личные кабинеты для пациентов
- Административная панель (Jazzmin)
- REST API для медицинских услуг
- Docker-контейнеризация

## 📋 Функционал

### Для пациентов:
- 📝 Регистрация и авторизация
- 📅 Запись на прием онлайн и отмена записей
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

cd medic_diagnostic

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

docker-compose -f docker-compose.yml up --build

- **Или для продакшена**

docker-compose up --build

Приложение будет доступно по адресу: http://localhost:8001


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

DATABASE_URL=postgres://пользователь_бд:пароль@localhost:5432/название_бд

## 👥 Тестовые пользователи
**После запуска create_test_data.py создаются:**
- Администратор: admin / admin123
- Врачи: dr_ivanov / doctor123, dr_petrova / doctor123
- Пациент: testuser / test123

## 📄 Лицензия
- MIT License

## 🎯 Демонстрация
- Список всех категорий услуг: /services/api/categories/
- Детали категории: /services/api/categories/{id}/
- Список всех активных услуг: /services/api/services/
- Детали услуги: /services/api/services/{id}/
- Фильтрация услуг по категории: /services/api/services/?category={id}