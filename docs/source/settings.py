INSTALLED_APPS=(
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_autocomplete',
    'django_autocomplete.tests',
    ),
DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
        }
    },
SECRET_KEY='#',
STATIC_URL = '/static/',
MIDDLEWARE_CLASSES=(
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ),
ROOT_URLCONF = 'django_autocomplete.tests.urls'

