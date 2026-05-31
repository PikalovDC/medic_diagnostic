import os
from pathlib import Path

from dotenv import load_dotenv

##from dotenv import load_dotenv  # Добавляем эту строку

# Загружаем переменные окружения из .env файла
load_dotenv()

AUTH_USER_MODEL = 'accounts.CustomUser'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# Секретный ключ из переменных окружения
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ваш-уникальный-ключ-для-медицинского-проекта-2025')

# Безопасность для Docker/продакшена
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Разрешённые хосты
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Приложения (пока добавляем, потом создадим)
    'main',
    'services',
    'appointments',
    'accounts',

    # Сторонние приложения
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
]

# Настройки crispy forms для Bootstrap 5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Получаем DATABASE_URL из переменных окружения или используем SQLite для разработки
##import os
##from urllib.parse import urlparse

# Для Docker используем DATABASE_URL, для локальной разработки - SQLite
##DATABASE_URL = os.environ.get('DATABASE_URL')

##if DATABASE_URL:
    # Парсим DATABASE_URL (формат: postgres://user:password@host:port/dbname)
##    url = urlparse(DATABASE_URL)

##    DATABASES = {
##        'default': {
##            'ENGINE': 'django.db.backends.postgresql',
##            'NAME': url.path[1:],  # убираем первый слэш
##            'USER': url.username,
##            'PASSWORD': url.password,
##            'HOST': url.hostname,
##            'PORT': url.port,
##        }
##    }
##else:
    # Локальная разработка без Docker - используем SQLite
##    DATABASES = {
##        'default': {
##            'ENGINE': 'django.db.backends.sqlite3',
##            'NAME': BASE_DIR / 'db.sqlite3',
##        }
##    }



# Простые настройки базы данных
USE_POSTGRESQL = False  # Поставьте True если хотите использовать PostgreSQL

if USE_POSTGRESQL:
    # Настройки PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'medical_db',
            'USER': 'medical_user',
            'PASSWORD': 'medical_password123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    # Настройки SQLite (проще для разработки)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }




# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Статические файлы (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
]

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Перенаправление после входа/выхода
LOGIN_REDIRECT_URL = '/'  # После входа - на главную
LOGOUT_REDIRECT_URL = '/'  # После выхода - на главную
LOGIN_URL = '/accounts/login/'  # URL для страницы входа

# Язык и время
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Форматы дат для России
DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i'
SHORT_DATE_FORMAT = 'd.m.Y'
SHORT_DATETIME_FORMAT = 'd.m.Y H:i'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Jazzmin
JAZZMIN_SETTINGS = {
    # Название сайта в заголовке
    "site_title": "МедДиагностика",

    # Заголовок на экране входа
    "site_header": "МедДиагностика",

    # Название бренда в боковом меню
    "site_brand": "🏥 МедДиагностика",

    # Логотип для сайта (положите logo.png в static/img/)
    "site_logo": "img/logo.png",

    # Приветственный текст на главной
    "welcome_sign": "Добро пожаловать в панель управления медицинским центром",

    # Авторские права
    "copyright": "Медицинский Диагностический Центр",

    # Поиск по моделям
    "search_model": ["services.Service", "services.ServiceCategory", "auth.User"],

    # ========== ВАЖНО: Боковое меню ==========
    "show_sidebar": True,  # Показывать боковое меню
    "navigation_expanded": True,  # Развернутые меню по умолчанию
    "order_with_respect_to": ["services", "auth"],

    # ========== ЦВЕТОВАЯ СХЕМА ==========
    # "dark_mode_theme": True,  # Раскомментируйте для темной темы

    # Светлая тема с мягкими цветами
    "theme": "flatly",  # Попробуйте также: "cosmo", "cerulean", "simplex", "minty"

    # Цвет кнопок и акцентов
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },

    # ========== ИКОНКИ ==========
    "icons": {
        # Приложения
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-md",
        "auth.Group": "fas fa-users",

        # Services
        "services.Service": "fas fa-stethoscope",
        "services.ServiceCategory": "fas fa-list-medical",

        # Accounts (если есть приложение accounts)
        "accounts.UserProfile": "fas fa-id-card",

        # По умолчанию
        "admin.LogEntry": "fas fa-history",
    },

    # Иконки по умолчанию для меню
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # ========== НАСТРОЙКИ ВНЕШНЕГО ВИДА ==========
    # Показывать кастомный UI
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,  # Включить UI-редактор (самое полезное!)

    # Ссылка "посмотреть на сайте"
    "show_view_on_site": True,

    # Редактирование из списка
    "changeform_format": "horizontal_tabs",  # horizontal_tabs, collapsible, carousel

    # Обновлять страницу при изменении
    "refresh_on_load": False,

    # Ширина бокового меню
    "sidebar_width": "280px",
}

# Дополнительные настройки UI
