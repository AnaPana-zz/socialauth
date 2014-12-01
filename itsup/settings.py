"""
Django settings for itsup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#x9j5hn3lf!0q@wak2gfpt!z5$nfaiswhz))2-7eqaix*r!^2i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', False)

TEMPLATE_DEBUG = os.environ.get('DJANGO_TEMPLATE_DEBUG', DEBUG)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'itsup.urls'

WSGI_APPLICATION = 'itsup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DJANGO_DB_NAME'],
        'USER': os.environ['DJANGO_DB_USER'],
        'PASSWORD': os.environ['DJANGO_DB_PASS'],
        'HOST': os.environ['PGSQL_HOST'],
        'PORT': os.environ['PGSQL_PORT'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/data/web/static'


# Logging

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
      'logstash': {
          'level': 'ERROR',
          'class': 'logstash.LogstashHandler',
          'host': os.environ['LOGSTASH_HOST'],
          'port': int(os.environ['LOGSTASH_UDP_PORT']),
          'version': 1,
          'message_type': 'logstash',
      },
  },
  'loggers': {
      'django': {
          'handlers': ['logstash'],
          'level': 'DEBUG',
          'propagate': True,
      },
  },
}
