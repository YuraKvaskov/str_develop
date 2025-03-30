from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
if os.getenv('DJANGO_LOG_DIR'):
    LOG_DIR = os.getenv('DJANGO_LOG_DIR')
else:
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
# os.makedirs(LOG_DIR, exist_ok=True)
# LOG_DIR = os.getenv('DJANGO_LOG_DIR', os.path.join(BASE_DIR, 'logs'))
# os.makedirs(LOG_DIR, exist_ok=True)
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = "/var/html/static/"
MEDIA_ROOT = "/var/html/media/"
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'api.apps.ApiConfig',
    'str.apps.StrConfig',
    'catalog.apps.CatalogConfig',
    'colorfield',
    'drf_spectacular',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # Рекомендуется для продакшн (1 год)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Если сайт использует поддомены
SECURE_HSTS_PRELOAD = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',

]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['https://stroymash-partners.ru']
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Проект Точки продаж АО Строймаш API',
    'DESCRIPTION': 'API для сервиса по поиску точек продаж Строймаш и каталога',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Дополнительные настройки
}

ROOT_URLCONF = 'StrProject.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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
WSGI_APPLICATION = 'StrProject.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

