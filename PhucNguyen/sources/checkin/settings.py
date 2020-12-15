"""
Django settings for checkin project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*q3obc_onkpv@a52wv@y3itw887ck--^h(zog$p6)hpnmmi=)9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'checkin.facecheckin.apps.FacecheckinConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'checkin.urls'

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

WSGI_APPLICATION = 'checkin.wsgi.application'
CORS_ORIGIN_ALLOW_ALL = True


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")]
TIMESHEET_PATH = os.path.join("static", "timesheet")
LOCATION = os.path.abspath(os.path.join(
    os.path.abspath(__file__), "..", "..", ".."))
PYTHONPATH = os.path.join(LOCATION, "sources")
STORAGE_ROOT = os.path.join(LOCATION, "storage")
STORAGE_LOCATION = os.path.join(STORAGE_ROOT, "images")
LOG_LOCATION = os.path.join(STORAGE_ROOT, "logs")
LOG_TRAINNING_PATH = os.path.join(LOG_LOCATION, "fci_trainning.log")
LOG_API_PATH = os.path.join(LOG_LOCATION, "fci_api.log")
LOG_STREAMING_PATH = os.path.join(LOG_LOCATION, "fci_streaming.log")
print("__________STORAGE_LOCATION", STORAGE_LOCATION)
print("__________STORAGE_ROOT", STORAGE_ROOT)

if not os.path.isdir(STORAGE_ROOT):
        os.mkdir(STORAGE_ROOT)
if not os.path.isdir(STORAGE_LOCATION):
        os.mkdir(STORAGE_LOCATION)

if not os.path.isdir(os.path.join(STORAGE_ROOT, "dbfaces")):
        os.mkdir(os.path.join(STORAGE_ROOT, "dbfaces"))

if not os.path.isdir(os.path.join(STORAGE_ROOT, "dbfeatures")):
        os.mkdir(os.path.join(STORAGE_ROOT, "dbfeatures"))

if not os.path.isdir(os.path.join(STORAGE_ROOT, "dbclassifiers")):
        os.mkdir(os.path.join(STORAGE_ROOT, "dbclassifiers"))

if not os.path.isdir(LOG_LOCATION):
        os.mkdir(LOG_LOCATION)

if not os.path.exists(LOG_TRAINNING_PATH):
        os.mknod(LOG_TRAINNING_PATH)
if not os.path.exists(LOG_API_PATH):
        os.mknod(LOG_API_PATH)
if not os.path.exists(LOG_STREAMING_PATH):
        os.mknod(LOG_STREAMING_PATH)

FACE_DIR = {
    "dbtemp": "dbtemp",
    "dbimages": "dbimages",
    "dbnormfaces": "dbnormfaces",
    "dbfeatures": "dbfeatures",
    "dbfaceclassifier": "dbfaceclassifier"
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(STORAGE_LOCATION), 'db.sqlite3'),
    }
}

API_ENDPOINT = {
    'SHOW_TIMESHEET': '/fci/data/show_timesheet',
    'GET_USERS': '/fci/data/get_users_information',
    'REGISTER_USER': '/fci/data/register_user',
    'SHOW_IMAGE': '/fci/data/show_image',
    'GET_ATTRIBUTE': '/fci/data/get_attributes',
    'DOWNLOAD_TIMESHEET': '/fci/data/download_timesheet',
    'VIDEO_STREAM': '/video_feed',
    'CAMERA_CONFIG_URL': '/fci/data/set_camera_config',
    'GET_USER_IMAGE': '/fci/data/get_user_images',
    'SHOW_USER_IMAGE': '/fci/data/show_user_image',
    'DELETE_USER_IMAGE': '/fci/data/delete_user_image',
    'CAMERA_CONFIG_ATTRIBUTES': '/fci/data/get_camera_config',
    'GET_UPDATE_USER_URL': '/fci/user'
}


LOCAL_TIMEZONE = "Asia/Bangkok"
MAXIMUM_LENGTH_IMAGE = 10
NUMMER_OF_EMPLOYEE = 100
MAXIMUM_FACE_PER_USER = 300
CHECKIN_TIME_DURATION = 300
RECENT_TIME_DURATION = 60*60*24  # 1 day

# Config domain webview
FCI_HOST = "172.16.1.4"
FCI_API_PORT = "8000"
FCI_STREAMING_PORT = "8001"