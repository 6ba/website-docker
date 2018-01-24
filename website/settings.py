import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '+a!s&fa0vzw2f243kwzppgmk+t$b#)pd=w0cnc&b1(816&tvqu'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.0.110', '192.168.100.202']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'compressor',
    'corsheaders',

    'proj',
    'accounts',
    'jtopot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'accounts.middleware.OnlineMiddleware',
]

ROOT_URLCONF = 'website.urls'

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
                # 全局过滤器全部舍弃
                #'accounts.context_processors.seo_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'djangobase2',
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# bootstrap颜色样式
BOOTSTRAP_COLOR_TYPES = [
    'default', 'primary', 'success', 'info', 'warning', 'danger'
]
SITE_ID = 1
SITE_ROOT = BASE_DIR
SITE_URL = "192.168.100.202:7788"
# 允许使用用户名或密码登录
# AUTHENTICATION_BACKENDS = ['accounts.user_login_backend.EmailOrUsernameModelBackend']

STATIC_ROOT = os.path.join(SITE_ROOT, 'collect_static')

STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')

# AUTH_USER_MODEL = 'accounts.ProjUser'
# LOGIN_URL = '/login/'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'

## 默认设置为 media
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '/collect_static/media')


from .personal_settings.compres_settings import *
from .personal_settings.email_setting import *
from .personal_settings.core_setting import *
from .personal_settings.auth_settings import *


import pymysql
MPP_CONFIG = {
    'host': '192.168.0.110',
    'user': 'root',
    'password': '112233..',
    'port': 22233,
    'db': 'qydldb',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

# MPP_CONFIG = {
#     'host': '192.168.0.101',
#     'port': 3306,
#     'user': 'admin007',
#     'password': 'myadmin@816',
#     'db': 'qydldb',
#     'charset': 'utf8',
#     'cursorclass': pymysql.cursors.DictCursor,
# }

# """生产环境数据库"""
# MPP_CONFIG = {
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'admin105',
#     'password': 'yesadmin@816',
#     'db': 'qydldb',
#     'charset': 'utf8',
#     'cursorclass': pymysql.cursors.DictCursor,
# }