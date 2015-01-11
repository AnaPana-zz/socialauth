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
    'social.apps.django_app.default',
    'user_auth_app',
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

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.dropbox.DropboxOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.vk.VKOAuth2',
    'social.backends.stackoverflow.StackoverflowOAuth2',
    'social.backends.email.EmailAuth',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'user_auth_app.CustomUser'

LOGIN_URL          = '/auth_app/login/'
LOGIN_REDIRECT_URL = '/auth_app/logged-in/'
LOGIN_ERROR_URL    = '/auth_app/login-error/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/auth_app/logout/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'

# These environment variables are different for production and local servers
# I've created two applications on all of the resources for testing on localhost and on Openshift
SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']  # facebook doesn't provide email address by default
# Note, that some facebook users can have unconfirmed email. In this case API wouldn't return it.

SOCIAL_AUTH_LINKEDIN_KEY = os.environ['SOCIAL_AUTH_LINKEDIN_KEY']
SOCIAL_AUTH_LINKEDIN_SECRET = os.environ['SOCIAL_AUTH_LINKEDIN_SECRET']
SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address']  # linkedin doesn't provide email address by default
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address')]


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']

SOCIAL_AUTH_GITHUB_KEY = os.environ['SOCIAL_AUTH_GITHUB_KEY']
SOCIAL_AUTH_GITHUB_SECRET = os.environ['SOCIAL_AUTH_GITHUB_SECRET']
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_DROPBOX_KEY = os.environ['SOCIAL_AUTH_DROPBOX_KEY']
SOCIAL_AUTH_DROPBOX_SECRET = os.environ['SOCIAL_AUTH_DROPBOX_SECRET']

SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ['SOCIAL_AUTH_VK_OAUTH2_KEY']
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_VK_OAUTH2_SECRET']
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_STACKOVERFLOW_KEY = os.environ['SOCIAL_AUTH_STACKOVERFLOW_KEY']
SOCIAL_AUTH_STACKOVERFLOW_SECRET = os.environ['SOCIAL_AUTH_STACKOVERFLOW_SECRET']


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


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
