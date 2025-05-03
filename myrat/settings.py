from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ojjg0_&=9sc#qys2a!f1#*yxvcy)p-t=@6*9msf6a@b=5^#da@'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    'drf_yasg',
    
    "accounts",
    "tasks",
    "clocks",
]

REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # )
}

AUTH_USER_MODEL = "accounts.User"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myrat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myrat.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myrat',
        'USER': 'avnadmin',
        'PASSWORD': 'AVNS_i_WyMkpTIFwaEBnvUAe',
        'HOST': 'delivery-kadyr-d419.l.aivencloud.com',
        'PORT': '10201',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / "static" ]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'
