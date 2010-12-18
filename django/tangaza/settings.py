#
#    Tangaza
#
#    Copyright (C) 2010 Nokia Corporation.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Authors: Billy Odero, Jonathan Ledlie
#

# Django settings for tangaza project.

import logging
import logging.config
import ConfigParser
import sys
import os

# TODO: Values for SMS_VOICE should be provided

# XXX make this somehow relative
# Causes error: NoSectionError: No section: 'formatters'
LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), 'logging.conf')

logging.config.fileConfig(LOGGING_CONFIG)

APP_CONFIG = os.path.join(os.path.dirname(__file__), '../../conf/settings.conf')

def read_config():
    parser = ConfigParser.ConfigParser()
    parser.read(APP_CONFIG)
    config_settings = {}
    
    for section in parser.sections():
        config_settings[section] = dict(parser.items(section))
        
    return config_settings

CFG_SETTINGS = read_config()


#Custom settings for sending sms
SMS_VOICE = {
    'SMS_USERNAME_KE': '',
    'SMS_PASSWORD_KE': '',
    'SMS_URL_KE': '',
    'SMS_FROM_KE': '',
    'SMS_SMSC_KE': '',
    'VOICE_KE': '',
    'modem-tangaza':'KE',

    'SMS_USERNAME_US': '',
    'SMS_PASSWORD_US': '',
    'SMS_URL_US': '',
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

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = CFG_SETTINGS['mysql']['db_name']             # Or path to database file if using sqlite3.
DATABASE_USER = CFG_SETTINGS['mysql']['db_user']             # Not used with sqlite3.
DATABASE_PASSWORD = CFG_SETTINGS['mysql']['db_pass']         # Not used with sqlite3.
DATABASE_HOST = CFG_SETTINGS['mysql']['db_host']  # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Nairobi'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

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
#SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

# Ledlie took out caching as we will not always want to respond the same way to the same request.
#    'django.middleware.cache.UpdateCacheMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'tangaza.sms.forms.ThreadLocals',
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
    'django.contrib.admindocs',
    'django.contrib.admin',
    'tangaza.sms',
)
