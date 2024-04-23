"""
Django settings for rpa_server project.

Generated by 'django-admin startproject' using Django 3.2.23.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 追加系统的导包路径(目的：1：注册子应用时可以写的方便一点 2：修改Django认证模型类时，必须以 应用名.模型名)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s10glo@wgx-z8jwkpo*^fk3eo&%-5&&%ci2*v*o_0ym@-hsbn)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # DRF
    'corsheaders',  # 解决跨域问题
    'django_filters',  # 过滤器
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rpa_server.urls'

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

WSGI_APPLICATION = 'rpa_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# HOST 8.138.134.118
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3390,  # 数据库端口
        'USER': 'rpa_server',  # 数据库用户名
        'PASSWORD': 'Aibang715926juejin666...',  # 数据库用户密码
        'NAME': 'rpa_server_v1',  # 数据库名字
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# redis配置
CACHES = {
    "default": {  #
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6356/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": 'Aibang715926juejin666...'
        }
    }, "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6356/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": 'Aibang715926juejin666...'
        }
    }, "cache": {  # 大体积请求体缓存
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6356/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": 'Aibang715926juejin666...'
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # 设置存储到内存，但是我使用了“SESSION_CACHE_ALIAS” 就被改成了存储到redis
SESSION_CACHE_ALIAS = "session"  # 告诉session  redis配置的别名

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
MEDIA_STATIC_URL = 'https://api.rpabang.com'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# media配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')  # 用于存储和访问上传图片的根目录

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 修改Django用户认证后端类
# AUTHENTICATION_BACKENDS = [
#     'users.utils.UsernameMobileAuthBackend',
# ]
#
# # 修改Django认证系统的用户模型类
AUTH_USER_MODEL = 'users.User'


# DRF配置
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'rpa_server.utils.exceptions.exception_handler',
    # 配置全局的认证方案
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # JWT认证
        'rest_framework.authentication.BasicAuthentication',  # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
    ),
    # # 配置限流方案
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    #     # 'verifications.throttling.CustomRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '60/min',
    #     'user': '60/min',
    #     # 'custom': '5/min',
    #     'custom': '3600/hour',
    # }
    # 分页
    # 'DEFAULT_PAGINATION_CLASS': 'meiduo_mall.utils.pagination.StandardResultsSetPagination',
}
# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'x-access-token',
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'X-Token',
)

# 解决跨域 CORS  需要在MIDDLEWARE添加 'corsheaders.middleware.CorsMiddleware'
CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://8.138.134.118:80"
    "https://rpabang.com"
    "http://rpabang.com"
    "https://api.rpabang.com"
    "http://api.rpabang.com"
)
CORS_ALLOWED_ORIGINS = [
    "https://rpabang.com",
    "http://rpabang.com",
]
CSRF_TRUSTED_ORIGINS = [
    'http://rpabang.com',
    'https://rpabang.com',
]

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 设置有效期
    # 修改JWT登陆视图的构造函数
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
    # 'JWT_PAYLOAD_HANDLER': 'user_management.utils.jwt_payload_handler_overwrite',
}

