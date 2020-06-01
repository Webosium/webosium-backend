from .base import *

DEBUG = False
ALLOWED_HOSTS = ['ipaddress']

CORS_ORIGIN_ALLOW = True
CORS_ORIGIN_WHITELIST =['ipaddress']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD':config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}