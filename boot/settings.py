"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import logging
import os
from pathlib import Path


# Basic Config
BASE_DIR = Path(__file__).resolve().parent.parent
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
STATIC_URL = 'static/'
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT',
                             os.path.join(BASE_DIR, 'static'))
MEDIA_ROOT = os.environ.get('DJANGO_STATIC_ROOT',
                            os.path.join(BASE_DIR, 'media'))
LOG_ROOT = os.environ.get('DJANGO_LOG_ROOR',
                           os.path.join(BASE_DIR, 'logs'))
ROOT_URLCONF = 'boot.urls'
RUNNING_ENV = os.environ.get('DJANGO_RUNNING_ENV', 'DEV')
RUNNING_JOB = os.environ.get('DJANGO_RUNNING_JOB', 'WEB_SERVER')
# USER_TEST is less strict but do not display debug info
if RUNNING_ENV not in ['DEV', 'TEST', 'USER_TEST', 'PRODUCT']:
    raise ValueError(f'Unsupported Debug level: {RUNNING_ENV}')
DEBUG = (RUNNING_ENV in ['DEV', 'TEST'])
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
DOMAIN = os.environ.get('DJANGO_DOMAIN', 'localhost')


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'account',
    'reminder',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Used for general templates
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        # Required by admin
        # Place templates in github is not a bad idea, so just let app
        #   use their own templates dir
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "boot.wsgi.application"


# Database & Auth
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DJANGO_DB', 'dev_db'),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'mysql'),
        'PORT': os.environ.get('DJANGO_DB_PORT', 3306),
        'USER': os.environ.get('DJANGO_DB_USER', 'root'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'changeme'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# Do not store timezone in db
USE_TZ = False

# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = 'account.Account'


# Security
SECRET_KEY = ('django-insecure-ixz=ho!2df*vpczj4t0mt0(a6hr8w4q4l4k(74iajrd5eh^b%0' 
                if DEBUG
                else os.environ['DJANGO_SECRET_KEY'])
ALLOWED_HOSTS = ['*'] if DEBUG else os.environ['DJANGO_ALLOWED_HOSTS'].split(':')
CSRF_TRUSTED_ORIGINS = [DOMAIN]