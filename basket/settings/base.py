from pathlib import Path
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_KEY = "-)9kk8+ezo!pms_mf#%3@*gd&lz6y&*jh-t+if#n6461y)wi70"
CORS_ORIGIN_ALLOW_ALL = True   


# CORS_ORIGIN_WHITELIST = [
#     'http://localhost',
#     'http://192.168.1.66:8000',
# ]

INSTALLED_APPS = [
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'django.contrib.sites',
    'django.contrib.sitemaps',

    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'mptt',

    'accounts',
    'product',
    'buyers_requests',
    'wishlist',
    'address',
    'vendor', 
    'home',
    'blog',
    'inbox',
]



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'compression_middleware.middleware.CompressionMiddleware',
]


ROOT_URLCONF = 'basket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.pages',
                'inbox.context_processors.unseen',
                'product.context_processor.sectors',
            ],
        },
    },
]

WSGI_APPLICATION = 'basket.wsgi.application'


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_L10N = True
USE_TZ = True


SITE_ID = 1


CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar_Full': [
#             ['Styles', 'Format', 'Bold', 'Italic', 'Underline',
#              'Strike', 'SpellChecker', 'Undo', 'Redo'],
#             ['Link', 'Unlink', 'Anchor'],
#             ['Image', 'Flash', 'Table', 'HorizontalRule'],
#             ['TextColor', 'BGColor'],
#             ['Smiley', 'SpecialChar'], ['Source'],
#             ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
#             ['NumberedList', 'BulletedList'],
#             ['Indent', 'Outdent'],
#             ['Maximize'],
#         ],
#         'extraPlugins': 'justify,liststyle,indent,Image, ImageResizeEditing, ImageResizeHandles',
#         'height': "auto",
#         'width': "auto",
#     },
# }

CKEDITOR_CONFIGS = {
    'default': {
        # 'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', 'Preview', 'Templates']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',]},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'about', 'items': ['About']},
            '/', 
            {'name': 'yourcustomtools', 'items': [
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': "auto",
        'width': "auto",
        'toolbarCanCollapse': True,
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', 
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
        ]),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = 'user_login'


INTERNAL_IPS = ["127.0.0.1","192.168.1.66","127.0.0.1:8000"]



STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, "media")




