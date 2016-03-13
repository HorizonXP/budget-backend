"""
Django settings for budget project.

Generated by 'django-admin startproject' using Django 1.9.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUDGET_PROD = True if os.environ.get('BUDGET_PROD', False) == 'True' else False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'svmo!dw+%%cu&oskbxri8(e$laa5$hn!x(7wb0&2d3io7*4-t&' if not BUDGET_PROD else os.environ.get('BUDGET_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
BUDGET_DEBUG_OVERRIDE = True if os.environ.get("BUDGET_DEBUG_OVERRIDE", False) == 'True' else False
DEBUG = BUDGET_DEBUG_OVERRIDE if BUDGET_PROD else True

ALLOWED_HOSTS = [] if not BUDGET_PROD else json.loads(os.environ.get('BUDGET_ALLOWED_HOSTS'))


# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
)

THIRD_PARTY_APPS = (
    'guardian',
    'rest_framework',
    'rest_framework.authtoken'
)

LOCAL_APPS = (
    'api',
    'budget'
)

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DEFAULT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware', # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
]

ROOT_URLCONF = 'budget.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'budget.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if BUDGET_PROD:
    from urllib.parse import urlparse

    # Expected format: postgresql://<username>:<password>@<private_ip>:<port>/<dbname>
    POSTGRESQL_URL = urlparse(os.environ.get('BUDGET_POSTGRESQL_URL'))
    REDIS_URL = urlparse(os.environ.get('BUDGET_REDIS_URL'))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': POSTGRESQL_URL.path.strip('/'),
            'USER': POSTGRESQL_URL.username,
            'PASSWORD': POSTGRESQL_URL.password,
            'HOST': POSTGRESQL_URL.hostname,
            'PORT': POSTGRESQL_URL.port,
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://%s:%s/0' % (REDIS_URL.hostname, REDIS_URL.port),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/backend/'

# django REST framework
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.DjangoObjectPermissions'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
}

import datetime
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'api.utils.jwt_response_payload_handler'
}

SITE_ID = 1

MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static/backend'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
