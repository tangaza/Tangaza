# Django settings for Test project.

import logging
import logging.config
import ConfigParser
import sys
import os

# set up some simple logging
DEBUG = True
#LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), 'logging.conf')
#logging.config.fileConfig(LOGGING_CONFIG)

logging.basicConfig(
    level = logging.DEBUG,
    format = '[%(asctime)s]:[%(levelname)s][%(name)s:%(lineno)d] %(message)s',
    filename = '/tmp/tangaza.log',
    filemode = 'a',
)

#APP_CONFIG = '/etc/tangaza/settings.conf'

def read_config():
    parser = ConfigParser.ConfigParser()
    parser.read(APP_CONFIG)
    config_settings = {}
    
    for section in parser.sections():
        config_settings[section] = dict(parser.items(section))
        
    return config_settings

#CFG_SETTINGS = read_config()

#Custom settings for sending sms
SMS_VOICE = {
    'SMS_USERNAME_KE': '',
    'SMS_PASSWORD_KE': '',
    'SMS_URL_KE': 'http://localhost/test.php',
    'SMS_FROM_KE': '',
    'SMS_SMSC_KE': '',
    'VOICE_KE': '',
    'modem-tangaza':'KE',

    'SMS_USERNAME_US': '',
    'SMS_PASSWORD_US': '',
    'SMS_URL_US': 'http://localhost/test.php',
    'SMS_FROM_US': '',
    'SMS_SMSC_US': '',
    'VOICE_US': '',
    'mosms':'US',

    'SMS_USERNAME_FI': '',
    'SMS_PASSWORD_FI': '',
    'SMS_URL_FI': '',
    'SMS_FROM_FI': '',
    'SMS_SMSC_FI':'',
    'VOICE_FI': '',
}


TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tangaza',                      # Or path to database file if using sqlite3.
        'USER': 'tzuser',                      # Not used with sqlite3.
        'PASSWORD': 'yourpass',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'TEST_CHARSET': 'UTF8',
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Nairobi'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cambp&0p2)q#3$nhomu6@hhu1)isw*itznm(^2$u8n(+4m=3hv'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'tangaza.Tangaza.forms.ThreadLocals'

)

ROOT_URLCONF = 'tangaza.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'tangaza.Tangaza',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTH_PROFILE_MODULE = 'Tangaza.Watumiaji'
