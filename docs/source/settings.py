INSTALLED_APPS=(
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_autocomplete',
    'django_autocomplete.tests',
    )
DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
        }
    }
SITE_ID = 303
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY='#'

