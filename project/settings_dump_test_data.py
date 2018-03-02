# encoding=utf-8


from settings import *

#TEST_ENVIRONMENT to True will make us not use the RealTimeSearchIndex
TEST_ENVIRONMENT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tmp_dasa',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
#         'HOST': '/tmp/',  #this is where the socket file can be found
#          'PORT': '5430',                      # Set to empty string for default. Not used with sqlite3.
    }
}
