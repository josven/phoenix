# -*- coding: utf-8 -*-
# Django settings for phoenix project.
from server_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sv-SE'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# DeprecationWarning
# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'phoenix.apps.notifications.middleware.AnnonuceNotifications',
    'phoenix.apps.core.middleware.AjaxRedirect',
    'phoenix.apps.registration.middleware.ActiveUserMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'phoenix.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/src/django-debug-toolbar/debug_toolbar/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'taggit',
    'south',
    'mptt',
    'sorl.thumbnail',
    'oembed',
    'reversion',
    'pagination',
    'debug_toolbar',
    'tastypie',
    'templatetag_handlebars',
    'bootstrap_toolkit',
    'phoenix.apps.core',
    'phoenix.apps.registration',
    'phoenix.apps.forum',
    'phoenix.apps.chat',
    'phoenix.apps.claim',
    'phoenix.apps.guestbook',
    'phoenix.apps.profiles',
    'phoenix.apps.articles',
    'phoenix.apps.accounts',
    'phoenix.apps.notifications',
    'phoenix.apps.mobile',
)

CACHE_COUNT_TIMEOUT = 60  # seconds, not too long.

AUTH_PROFILE_MODULE = 'profiles.profile'

AUTHENTICATION_BACKENDS = ('phoenix.apps.accounts.views.CaseInsensitiveModelBackend',)

LOGIN_REDIRECT_URL = '/'

# debug_toolbar.middleware.DebugToolbarMiddleware use this to determine your IP. 

INTERNAL_IPS = ('192.168.1.70','127.0.0.1')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

#Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'phx.mailer@gmail.com'
EMAIL_HOST_PASSWORD = 'fiskenflyger'
EMAIL_PORT = 587

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
