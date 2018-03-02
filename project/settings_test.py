# encoding=utf-8
from settings_local import *  # @UnusedWildImport

THUMBNAIL_DEBUG = False

INSTALLED_APPS.append('django_nose')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dasa',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',  # this is where the socket file can be found
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


TEST_ENVIRONMENT = True

REPOSITORY_URL = 'http://127.0.0.1:5000/'

SOUTH_TESTS_MIGRATE = False # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True # To disable South's own unit tests

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'
    },
}
