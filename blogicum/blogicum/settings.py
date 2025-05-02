from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-3e($2iv1#9kguloseoq)5(k6ydnqy5d3fg&-3sbg1zyb2c329r'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # Подключение приложения Blog.
    'pages.apps.PagesConfig',  # Подключение приложения Pages.
    'core.apps.CoreConfig',  # Подключение приложения Core.
    'debug_toolbar',  # Установка Django Debug Toolbar.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Установка Django Debug Toolbar.
]

INTERNAL_IPS = [
    '127.0.0.1',  # Обработка запросов с localhost.
]

ROOT_URLCONF = 'blogicum.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'  # Перенос папки шаблонов на уровень проекта.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogicum.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-RU'  # Перевод языка админ панели на русский язык.

TIME_ZONE = 'Asia/Yekaterinburg'  # Смена часового пояса на МСК+2.

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static_dev/'  # Перенос статических файлов на уровень проекта.

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev/',  # Указание Django где искать статические файлы проекта.
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
