"""
Django settings for savannah project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$2f0-ie0xkn__5sy1r*ypak(8v5v8&^@awp#*6^tkub6pyyr7^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALPHA = False
BETA = True
OPEN_BETA = True
IS_DEMO = False
DEMO_POOL = 3
DEMO_DURATION_HOURS = 24
DEMO_SIZE = 500
SITE_ROOT = os.environ.get('SITE_ROOT')
SITE_DOMAIN = os.environ.get('SITE_DOMAIN')
SITE_NAME = os.environ.get('SITE_NAME')
SYSTEM_USER = os.environ.get('SYSTEM_USER')
FONTAWESOME_KIT_URL = 'https://kit.fontawesome.com/a160749d77.js'

PUBLIC_EMAIL_DOMAINS = [
    'gmail.com',
    'googlemail.com',
    'outlook.com',
    'outlook.fr',
    'outlook.de',
    'live.com',
    'live.fr',
    'live.de',
    'yahoo.com',
    'yahoo.co.uk',
    'yahoo.com.br',
    'yahoo.fr',
    'yahoo.de',
    'aol.com',
    'mac.com',
    'mail.ru',
    'mail.com',
    'yandex.ru',
    'yandex.com',
    'me.com',
    'hotmail.com',
    'hotmail.co.uk',
    'hotmail.fr',
    'hotmail.de',
    'icloud.com',
    'protonmail.com',
    'qq.com',
    '163.com',
    '126.com',
    'gmx.com',
    'gmx.net',
    'gmx.de',
    'free.fr',
    'web.com',
    'web.fr',
    'web.de',
]
COMPANY_SUGGESTION_MATCHES = 3

ALLOWED_HOSTS = []
ALLOWED_EMAILS_PER_DAY = 100
DEFAULT_FROM_EMAIL = "SavannahHQ <noreply@savannahhq.com>"
EMAIL_CONFIRMAION_EXPIRATION_DAYS = 10
PASSWORD_RESET_EXPIRATION_DAYS = 1

MAX_CHANNEL_IMPORT_FAILURES = 24
MAX_SOURCE_IMPORT_FAILURES = 48
MAX_IMPORT_HISTORY_DAYS=180

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    'rest_framework',
    "imagekit",
    "imagekit_cropper",
    'notifications',
    'crispy_forms',
    'totd',
    'simple_ga',
    'markdownify.apps.MarkdownifyConfig',

    'corm.apps.CormConfig',
    'frontendv2.apps.FrontendConfig',
    'apiv1.apps.Apiv1Config',
    'demo.apps.DemoConfig',

    'djstripe',
    'billing.apps.BillingConfig',
]

CORM_PLUGINS = [
    "corm.plugins.discord.DiscordPlugin",
    "corm.plugins.discourse.DiscoursePlugin",
    "corm.plugins.github.GithubPlugin",
    "corm.plugins.gitlab.GitlabPlugin",
    "corm.plugins.facebook.FacebookPlugin",
    "corm.plugins.ical.iCalPlugin",
    "corm.plugins.meetup.MeetupPlugin",
    "corm.plugins.reddit.RedditPlugin",
    "corm.plugins.rss.RssPlugin",
    "corm.plugins.slack.SlackPlugin",
    "corm.plugins.stackexchange.StackExchangePlugin",
    "corm.plugins.salesforce.SalesforcePlugin"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "simple_ga.middleware.GAEventMiddleware",
    "frontendv2.middleware.ReadNotificationMiddleware",
]

ROOT_URLCONF = 'savannah.urls'

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
                "totd.context_processors.tips",
                "simple_ga.context_processors.events",
                "frontendv2.context_processors.colors",
                "frontendv2.context_processors.fonts",
            ],
        },
    },
]

WSGI_APPLICATION = 'savannah.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login/'

MESSAGE_TAGS = {
    messages.DEBUG: "alert-debug",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

DJANGO_NOTIFICATIONS_CONFIG = { 
    'USE_JSONFIELD': True
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './static/'
MEDIA_ROOT = "./media/"
MEDIA_URL = "/media/"

SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
SLACK_SCOPE = 'channels:history,channels:read,users:read'

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
GITHUB_SCOPE = "read:org,public_repo"

TOTD_EXCLUDE_NS = ['admin']

DJSTRIPE_WEBHOOK_EVENT_CALLBACK = "billing.callbacks.stripe_event_callback"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = 'id'

DJSTRIPE_WEBHOOK_SECRET = os.environ.get('DJSTRIPE_WEBHOOK_SECRET')
STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY')
STRIPE_LIVE_SECRET_KEY = os.environ.get('STRIPE_LIVE_SECRET_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

DISCORD_CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
DISCORD_APP_SECRET = os.environ.get('DISCORD_APP_SECRET')
DISCORD_BOT_SECRET = os.environ.get('DISCORD_BOT_SECRET')

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass
