from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['basketnepal.com','www.basketnepal.com',"127.0.0.1"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'basketnepal',
        'USER': 'basketnepaluser',
        'PASSWORD': 'surajbh71@',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}

 
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_HSTS_PRELOAD = True

##############################################


#SECURE_BROWSER_XSS_FILTER = True
# CORS_REPLACE_HTTPS_REFERER = True
# HOST_SCHEME = "https://"
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_FRAME_DENY = True


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

