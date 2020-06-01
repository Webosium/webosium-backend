from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '192.168.0.101']

CORS_ORIGIN_ALLOW = True
CORS_ORIGIN_WHITELIST =['http://localhost:3000', 'http://192.168.0.101:3000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}