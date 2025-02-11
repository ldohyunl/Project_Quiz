"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ytyx1edm3y_&9f_b2nu57*abbmbuh9_6h@!6-$on249r!m@+*u"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #app 추가
    "login",
    "main_page",
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 추가함
    'allauth',
    'django.contrib.sites',  # 필수
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1  # Django Site Framework 사용 시 일치하도록 설정

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"], # 기본 templates 디렉토리 추가
        "APP_DIRS": True, # 앱 내부의 templates 폴더도 인식하도록 설정
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysql 엔진 설정
        'NAME':'quiz_db', # 데이터베이스 이름
        'USER':'root', # 데이터베이스 연결시 사용할 유저 이름
        'PASSWORD':'0000sql', # 유저 패스워드		
        'HOST':'127.0.0.1', 
        'PORT':'3306'
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 이거 추가함 django-allauth
AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'naver': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': 'Etv6IXLgKpXnUM2scaQT',
#             'secret': 'Etv6IXLgKpXnUM2scaQT',
#             'key': ''
#         }
#     }
# }

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myapp/static'),
]

LOGIN_REDIRECT_URL = '/' # 추가 로그인 후 리다이렉트 할 페이지 주소 적기
LOGOUT_REDIRECT_URL = '/' # 로그아웃 후 리다이렉트 할 페이지 주소 적기

SOCIALACCOUNT_LOGOUT_ON_GET = True  # True로 설정하면 GET 방식으로 소셜 로그아웃이 처리됨
SOCIALACCOUNT_LOGIN_ON_GET = True # 중간 로그인 페이지 건너 뛰기 여부 
ACCOUNT_LOGOUT_ON_GET = True 

SITE_ID = 1


SOCIALACCOUNT_PROVIDERS = {
    'naver': {
        'APP': {
            'client_id': 'Etv6IXLgKpXnUM2scaQT',
            'secret': 'mvXEzAf_CR',
            'key': ''
        }
    },
    'kakao': {
        'APP': {
            'client_id': '카카오 REST API 키',
            'secret': '카카오 Secret Key',
            'key': ''
        }
    }
}
