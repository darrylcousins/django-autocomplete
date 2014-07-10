#!/usr/bin/env python
# thanks to https://github.com/carljm/django-model-utils
import os
import sys

from django.conf import settings
import django


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
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
        'django.contrib.auth.middleware.AuthenticationMiddlewarer'
        ),
    )


def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = ['django_autocomplete.tests']
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ['tests']

    do_coverage = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'coverage':
            do_coverage = True

    if do_coverage:
        from coverage import coverage
        cov = coverage(include='django_autocomplete/*')
        cov.start()

    failures = runner_class(
        verbosity=1, interactive=True, failfast=False).run_tests(test_args)

    if do_coverage:
        cov.stop()
        cov.report()

    sys.exit(failures)


if __name__ == '__main__':
    runtests()
