from .base import *


DEBUG = False

ALLOWED_HOSTS = ['cineplus.luisrubiodev.tech', '127.0.0.1','146.190.120.160', '46.202.150.5']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
