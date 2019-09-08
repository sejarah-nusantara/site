# Django settings for project project.

import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

#
# ADMINS: A tuple that lists people who get code error notifications. When DEBUG=False and a view raises an exception,
# Django will email these people with the full exception information.
#
ADMINS = (
    ('Jelle Gerbrandy', 'jellegerbrandy@gmail.com'),
)

SERVER_EMAIL = 'django@sejarah-nusantara.anri.go.id'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dasa',
        'USER': '',
        'PASSWORD': '',
        #        'HOST': '/tmp/',  #this is where the socket file can be found
        #        'PORT': '5430',                      # Set to empty string for default. Not used with sqlite3.
    },
    #     'default2': {
    #         'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    #         'NAME': 'dasa',  # Or path to database file if using sqlite3.
    #         'USER': '',  # Not used with sqlite3.
    #         'PASSWORD': '',  # Not used with sqlite3.
    #         'HOST': '',  # this is where the socket file can be found
    #         'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    #     }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
# TIME_ZONE = 'America/Chicago'
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html


LANGUAGE_CODE = 'en'
DEFAULT_LANGUAGE_CODE = 'en'
ADMIN_LANGUAGE_CODE = 'en'

#
# We cannot change the order of the languages without messsing up saving in backed
#
LANGUAGES = (
    ('en', 'English'),
    ('id', 'Bahasa Indonesia'),
)
#

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True
USE_THOUSANDS_SEPARATOR = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

MEDIA_ROOT = os.path.abspath(os.path.join(_PROJECT_DIR, '..', 'user_media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# THIS PATH IS RELATIVE TO MEDIA_ROOT
# UPLOAD_TO = 'uploads'  # upload files here
UPLOAD_TO = '.'

# DO NOT USE A SLASH AT THE BEGINNING, DO NOT FORGET THE TRAILING SLASH AT THE END.
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_VERSIONS_BASEDIR = '_versions'
FILEBROWSER_EXCLUDE = ['_versions', 'cache']
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx', '.kml', '.kmz', '.xlsx', '.xml', '.ods', '.odt'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
}


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(_PROJECT_DIR, '..', 'static')


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".

# this prefix messes up rosetta (Who sets it herself). Not setting it here does not seem to break anything else
# ADMIN_MEDIA_PREFIX = '/static/admin/'
# ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
# ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(_PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')#k0-1c3+j@#yz1t&2f43+9y3r%pdi7*#!ul%#dn@c8bfuz*fc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    'apptemplates.Loader',  # https://bitbucket.org/wojas/django-apptemplates
)

MIDDLEWARE_CLASSES = [
    'dasa.middleware.set_language.SetAdminLanguage',
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

]

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "templates"),
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.core.context_processors.static',
    'dasa.context_processors.dasa_context',
    'django.contrib.messages.context_processors.messages',
)


INSTALLED_APPS = [
    'localeurl',  # Because the application needs to replace the standard urlresolvers.reverse function, it is important to place it at the top of the list:
    'haystack',  # haystack first as a workaround for this issue: https://github.com/toastdriven/django-haystack/issues/84
    'dasa',
    'userena',  # userena before dasa to connect dasa admin hooks
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'filebrowser',  # needs to be before django.contrib.admin
    'django.contrib.admin',
    'tinymce',
    'sorl.thumbnail',
    'mce_filebrowser',
    'modeltranslation',
    'south',  # for db migration
    'sorl.thumbnail',
    'selectable',  # make nice comboboxes
    'django_date_extensions',
    'guardian',
    'easy_thumbnails',
    'django_countries',
]


MODELTRANSLATION_TRANSLATION_REGISTRY = "dasa.translation"


def skip_zodb_conflict_errors(record):
    if record.msg:
        if 'ConflictError' in record.msg:
            return False
    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'skip_zodb_conflict_errors': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_zodb_conflict_errors,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_zodb_conflict_errors'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.abspath(os.path.join(THIS_DIR, '..', 'var/log/django.log')),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'repository.interaction': {
            'handlers': ['mail_admins', 'logfile', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile',],
            'level': 'DEBUG',
            'propagate': True,
        },

    }
}

# http://django-tinymce.googlecode.com/svn/tags/release-1.5/docs/.build/html/installation.html#id2
# TINYMCE_JS_URL = 'http://debug.example.org/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace,fullscreen",
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    # see here fore buttons:
    # http://www.tinymce.com/wiki.php/TinyMCE3x:Buttons/controls
    'theme_advanced_buttons1': "bold,italic,underline,|,link,unlink,|,image,|,table,bullist,numlist,|,undo,redo,|,pasteword,|,charmap,code,|,fullscreen,",
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'extended_valid_elements': "video[*],source[*]",
    'file_browser_callback': 'mce_filebrowser',
    'theme_advanced_path': False,  # this setting is supposed to suppress that path in the status bar, but seems to have no effect
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_resizing': 'true',
    'file_browser_callback': 'CustomFileBrowser',
}
# TINYMCE_SPELLCHECKER = True
#
# TODO: upgrade tinymce on new release and the next issue is solved:
# cf. https://github.com/aljosa/django-tinymce/issues/59
TINYMCE_COMPRESSOR = False


# http://packages.python.org/django-localeurl/setup.html#configuration

PREFIX_DEFAULT_LOCALE = False

# for grappelli
# http://readthedocs.org/docs/django-grappelli/en/latest/quickstart.html#installation

GRAPPELLI_ADMIN_TITLE = 'DASA Admin'
GRAPPELLI_INDEX_DASHBOARD = 'project.grappelli_dashboard.MyDashboard'

# HAYSTACK_SITECONF = 'project.haystack_conf'
# HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:9024/solr'
THUMBNAIL_DEBUG = False
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_PREFIX = 'cache/'

HAYSTACK_CUSTOM_HIGHLIGHTER = 'dasa.utils.DasaHighlighter'

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:9024/solr',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}

PATH_TO_INGBOOK_PRODUCT = os.path.abspath(os.path.join(THIS_DIR, '..', 'src/INGBook/Products'))
#
# the next setting is useful if we want to do 'live' translation..
#
ROSETTA_WSGI_AUTO_RELOAD = False
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
ROSETTA_MESSAGES_PER_PAGE = 20

LOGIN_URL = '/admin/'
ROSETTA_URL = '/rosetta/'

# TODO: this should pick up formats in local.id.settings for the django backend, but it does not seem so
FORMAT_MODULE_PATH = 'locale'

LANGUAGE2EAD = {
    'en': 'icaatom-dasa.anri.go.id_339.ead.xml',
    'nl': 'icaatom-dasa.anri.go.id_383.ead.xml',
    'id': 'icaatom-dasa.anri.go.id_386.ead.xml',
}

# the id of the archive int he repository witht the ANRI data
ARCHIVE_IDS = {
    'K66a': '1',
    'CorpusDipl': '3',
    'DeHaan': '11'
}


#
# settings for userena
# http://docs.django-userena.org/en/latest/settings.html
#

AUTHENTICATION_BACKENDS = [
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PROFILE_MODULE = 'dasa.UserProfile'
ANONYMOUS_USER_ID = -1
ANONYMOUS_USER_ID = None

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'


USERENA_USE_MESSAGES = False
# USERENA_REGISTER_PROFILE = False
USERENA_REGISTER_USER = False

USE_X_FORWARDED_HOST = True

IMAGE_FIELDS = [
    ('models.BasicPage', ['image', 'image_description']),
    ('models.News', ['image', 'image_description']),
    ('models.HartaKarunCategory', ['image', 'image_intro']),
    ('models.HartaKarunMainCategory', ['image', 'image_intro']),
    ('models.HartaKarunItem', ['image', 'pdf', 'pdf_id']),
    ('models.LightBoxItem', ['image']),
    ('models.Scan', ['image']),
]

TEXT_FIELDS = [
    ('models.BasicPage', ['content']),
    ('models.News', ['content']),
    ('models.HartaKarunCategory', ['longIntroText']),
    ('models.HartaKarunMainCategory', ['longIntroText']),
    ('models.HartaKarunItem', ['introduction']),
]

ALLOWED_HOSTS = [
    'localhost',
    '.dc-dottcom.org',
    '127.0.0.1:8000', '127.0.0.1', '.sejarah-nusantara.anri.go.id', '.cortsfoundation.org', '.anri.id', '.sejarah-nusantara.anri.go.id.',
    '.gerbrandy.com',
    ]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =   'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'webmasterdasa@gmail.com'
EMAIL_HOST_PASSWORD = '7u4cgZ081bc294z'
