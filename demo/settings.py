import os


ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'django_countries',
    'core',
    'rest_framework',
    'tracking',
    'maps',
    'django_google_maps',
    'search2',
    'video_app',
    'image'
    
]

MIDDLEWARE = [
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

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
                'django.template.context_processors.request',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# static files (CSS, JS, Image)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': '666'
        }
    }
}

# CRISPY FORM

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STRIPE_PUBLIC_KEY = 'pk_test_bR1DE94niBsIEz2lMpO7KVal00Tf0f6d1m'
STRIPE_SECRET_KEY = 'sk_test_GpFIT8I0DkPrd1mOiN0IoIkI00hCrkCid9'

GOOGLE_MAPS_API_KEY = 'AIzaSyC74lMb-qCFqWVzjVJ7V_Y_f-3DZXMXzH8'

TWILIO_ACCOUNT_SID = os.getenv("ACc9d90a750508d1587a60d33176e04fea")
TWILIO_AUTH_TOKEN = os.getenv("f471d37c55a6f4cf47f3d8893e9378ac")
TWILIO_NUMBER = os.getenv("13344878514")
SMS_BROADCAST_TO_NUMBERS = [ 
    "+13022872114", # use the format +19735551234
    "+16466755860", 
    "+19177559465", 
]


## recommendation system
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1


# import keras
# import numpy as np
# from tensorflow.keras import backend as K
# from tensorflow.keras import tensorflow_backend
# import tensorflow as tf
# from tensorflow.python.keras.backend import set_session
# from keras.applications import vgg16


# def get_session():
#     config = tf.ConfigProto()
#     config.gpu_options.allow_growth = True
#     return tf.Session(config=config)

# K.tensorflow_backend.set_session(get_session())

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# SESS = tf.Session(config=config)
# print("model loading")
# GRAPH1 = tf.get_default_graph()

# set_session(SESS)
# # Load the VGG model
# VGG_MODEL = vgg16.VGG16(weights="imagenet")