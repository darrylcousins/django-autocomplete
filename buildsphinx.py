#!/usr/bin/env python
# thanks to https://github.com/carljm/django-model-utils
import os
import sys

from django.conf import settings
import django


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        'django_autocomplete',
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
        'django.contrib.auth.middleware.AuthenticationMiddlewarer'
        ),
    )


def buildsphinx():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from sphinx import main
    source = os.path.join(parent, 'docs/source')
    output = os.path.join(parent, 'docs/build/html')

    argv = ['-b html', source, output]
    sys.exit(main(argv))

if __name__ == '__main__':
    buildsphinx()
