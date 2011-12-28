# Modify this file and rename it server_settings.py

ADMINS = (
    # ('Jonas Svensson', 'jonas.s.svensson@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/josven/res/db/phoenix.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Caches needed for tumbnails
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/josven/res/cache/django_cache',
    }
}

# Absolute paths
# 
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/josven/res/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/josven/res/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+slmdspjJ0?lksH5¤tx9!!1alka97n3Jdc1?*0k35k%qelz&dtfz'