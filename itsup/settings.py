"""
Django settings for itsup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from .credentials import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ON_OPENSHIFT = False
if os.environ.get('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True


if ON_OPENSHIFT:
    DEBUG = False
else:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

if ON_OPENSHIFT:
    ALLOWED_HOSTS = [
        '.rhcloud.com',  # Allow domain and subdomains
    ]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#x9j5hn3lf!0q@wak2gfpt!z5$nfaiswhz))2-7eqaix*r!^2i'


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
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    #'custom_middlewares.middlewares.CatchSocialAuthExceptionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, 'templates')),
)

ROOT_URLCONF = 'itsup.urls'

WSGI_APPLICATION = 'itsup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if ON_OPENSHIFT:
    # os.environ['OPENSHIFT_POSTGRESQL_DB_*'] variables can be used with databases created
    # with rhc cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.environ['OPENSHIFT_APP_NAME'],  # Or path to database file if using sqlite3.
            'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],                      # Not used with sqlite3.
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],                  # Not used with sqlite3.
            'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'itsup.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
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

if ON_OPENSHIFT:
	STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')

STATICFILES_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, 'static')),
)

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

LOGIN_URL          = '/user_account/login/'
LOGIN_REDIRECT_URL = '/user_account/logged-in/'
LOGIN_ERROR_URL    = '/user_account/login-error/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/user_account/logout/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'

# These environment variables are different for production and local servers
# I've created two applications on all of the resources for testing on localhost and on Openshift
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']  # facebook doesn't provide email address by default
# Note, that some facebook users can have unconfirmed email. In this case API wouldn't return it.

SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address']  # linkedin doesn't provide email address by default
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address')]

SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']


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

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

