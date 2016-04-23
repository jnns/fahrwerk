"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # add --nostatic option to runserver
    'django.contrib.staticfiles',
    'fwk',
    'django_extensions',
    'debug_toolbar',
    'pipeline',
    'rest_framework',
    'formtools',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# This is the place where all static assets are collected to when
# 'django.contrib.staticfiles' is used.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'fwk': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

PIPELINE = {
    #'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
              'css/main.css',
            ),
            'output_filename': 'main.css',
            'extra_context': {
                'media': 'screen,projection'
            },
            'variant': 'datauri'
        }
    },
    'JAVASCRIPT': {
        'main': {
            'source_filenames': (
                'js/jquery.min.js',
                'js/underscore-min.js',
                'js/babel/browser.min.js',
                'js/react.min.js',
                'js/react-dom.min.js',
            ),
            'output_filename': 'main.min.js',
        },
        'map': {
            'source_filenames': {
                'js/map.js'
            },
            'output_filename': 'map.min.js',

        }
    },
    'YUGLIFY_BINARY': 'node_modules/yuglify/bin/yuglify',

    # This is important because Leaflet refuses to work when the scripts (I
    # have no idea which) are wrapped.
    'DISABLE_WRAPPER': True
}

EMAIL_SUBJECT_PREFIX = "[FWK] "

# This is Fahrwerk's landline that's used in several places throughout the
# codebase.
FWK_PHONE_NO = "(030) 40 58 51 00"

FWK_INFO_EMAIL = "info@fahrwerk-berlin.de"

# When NOT to display a page that says we're closed and that they should come
# back later.
FWK_OPENING_HOURS = {
    'Mon': ("07:30", "20:00"),
    'Tue': ("07:30", "20:00"),
    'Wed': ("07:30", "20:00"),
    'Thu': ("07:30", "20:00"),
    'Fri': ("07:30", "20:00"),
    'Sat': ("18:00", "20:00"),
    'Sun': (), # we're closed the whole day
}
