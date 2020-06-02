from .base import *

DEBUG = False
ALLOWED_HOSTS = ['139.59.16.121', 'backend.webosium.xyz']

CORS_ORIGIN_ALLOW = True
CORS_ORIGIN_WHITELIST =['http://localhost:3000', 'https://webosium.xyz', 'https://www.webosium.xyz']

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
