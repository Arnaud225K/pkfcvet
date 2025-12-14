import os
import getpass
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!


USER_NAME = getpass.getuser()
PROJECT_NAME = 'pkfcvet'

# Cookie name. This can be whatever you want.
SESSION_COOKIE_NAME = 'sessionid'
# The module to store sessions data.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Age of cookie, in seconds (default: 2 weeks).
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# Whether a user's session cookie expires when the Web browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False

CACHE_TIME_BASE = 60*60*2*1
CACHE_TIME_BASE_VIEW = 60 * 10

# EMAIL_HOST = 'mail.pkfcvet.ru'
# EMAIL_HOST_USER = "z@pkfcvet.ru"
# EMAIL_HOST_PASSWORD = "wLJJEqke7bxsozC"


PRODUCTS_PER_PAGE = 20
PRODUCTS_PER_ROW = 6

ID_MENU_MARKA_GOST = 79
SITE_ID = 1

SITE_NAME = 'ПФ Квет'
VERSION_NAME = 'Вер. 2.0 от 15.12.2025'
START_YEAR = "2017"
META_KEYWORDS = 'Цветной металлопрокат'
META_DESCRIPTION = 'ПФ Квет - отличный поставщик цветного металлопроката'

ERROR_CONSENT = "*Согласие на обработку: Обязательное поле."
CONTACTS_SESSION_KEY = 'contacts_clid'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


HOST_NAME = 'localhost'
MEDIA_URL = '/media/'

USE_CACHE = False


DEBUG = True



ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^=(nnare2&88yu7$^cq*6722z-ggm3riyfpzneo9!m@88a+=%^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'cacheops',
    'tinymce',
    'robots',
    'typemenu',
    'Marochnik',
    'GOST',
    'menu',
    'slider',
    'cart',
    'checkout',
    'News',
    'TextBlockUrl',
    'TextBlockMenu',
    'TypeTextBlock',
    'portfolio',
    'Contacts',
    'Sertificats',
    'stats',
    'search',
    'Filials',
    'Partners',
    'advanteges',
    'manufactures',
    'awards',
    'vacancy',
    'photogallery',
    'videogallery',
    'sotrudniki_service',
    'Pricelists',
    'catalog_filter',
    'import_control',
    'admin_m',
    'project_settings',
    'static_text',
    'SpecPredlozhenie',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'menu.custom_redirect_middleware.CustomRedirectFallbackMiddleware',
]



ROOT_URLCONF = 'pkfcvet.urls'

X_FRAME_OPTIONS = 'ALLOW_ALL'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'admin_m.views.static_admin_url',
                PROJECT_NAME + ".views.global_views",
                'static_text.views.static_text',
            ],
        },
    },
]

WSGI_APPLICATION = 'pkfcvet.wsgi.application'





# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-RU'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'

MEDIA_URL = '/media/'

WWW_ROOT ='www/'



MEDIA_ROOT = os.path.join(BASE_DIR, "www/media/")

STATIC_ROOT = os.path.join(BASE_DIR, "www/static/")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)




TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'height': "300",
    'plugins': 'fullscreen',
    'forced_root_block': '',
    'extended_valid_elements': "figure[*],use[*],svg[*]"
}
TINYMCE_INCLUDE_JQUERY = False



try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *


if USE_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            'TIMEOUT': 60,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "MAX_ENTRIES": 1000,
            }
        }
    }

    # SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

    CACHEOPS_REDIS = "redis://localhost:6379/1"

    CACHEOPS = {
        'Contacts.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'CatalogNew.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'menu.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'TypeTextBlock.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'TextBlockMenu.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'TypeMenu.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'PositionMenu.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'Partners.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'News.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'Marochnik.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'SpecPredlozhenie.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'Filials.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'django_ipgeobase.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'TextBlockCatalogCity.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'IzdelieProduct.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'robots.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'GOST.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'Sertificats.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'analitics.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'catalog_filter.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'cart.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'Slider.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        'Price.*': {'ops': 'all', 'timeout': CACHE_TIME_BASE},
        # '*.*': {'timeout': 60*60},
    }

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
        'template_timings_panel',
    )
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    # Предыдущие настройки логирования
    # LOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': False,
    #     'handlers': {
    #         'console': {
    #             'class': 'logging.StreamHandler',
    #         },
    #     },
    #     'loggers': {
    #         'django.db.backends': {
    #             'level': 'DEBUG',
    #             'handlers': ['console'],
    #         }
    #     },
    # }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'class': 'logging.FileHandler',
                'filename': 'server.log',
            },
            'console': {
                'class': 'logging.StreamHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'logfile'],
            },
        },
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    ]

    INTERNAL_IPS = ('127.0.0.1','46.48.62.141','5.165.24.207', '46.48.126.42')



    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
    INTERNAL_IPS = ('127.0.0.1',)


    
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

ORDER_NOTIFICATION_EMAIL = 'kouakanarnaud@gmail.com'





# CONFIGURATION DE CELERY
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'Asia/Yekaterinburg'
CELERY_ENABLE_UTC = True

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True