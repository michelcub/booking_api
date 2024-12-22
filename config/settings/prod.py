import os
from .base import *


DEBUG = True

SECRET_KEY = 'django-insecure-zj$vd*c!nkcha+tt$yg%c%a#=9ji2%xlqu8l)g(^h1(ors+%-g'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}