# -*- coding: utf-8 -*-
import unittest
import doctest

from django.test import RequestFactory
from django.contrib.auth.models import User
from django.test import Client

from django_autocomplete.tests.models import TestModel
from django_autocomplete.tests.models import TestFKModel


def setUp(test):
    test.globs['request_factory'] = RequestFactory()
    test.globs['TestModel'] = TestModel
    test.globs['TestFKModel'] = TestFKModel
    test.globs['Client'] = Client
    test.globs['User'] = User


def tearDown(test):
    pass


def load_tests(loader, tests, ignore):
    list_of_doctests = [
        'django_autocomplete.views',
        'django_autocomplete.widgets',
        'django_autocomplete.meta',
        'django_autocomplete.urls',
        ]
    suite = unittest.TestSuite()
    for t in list_of_doctests:
        tests.addTest(doctest.DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"]),
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))

    list_of_docfiles = [
        ]
    for t in list_of_docfiles:
        tests.addTest(doctest.DocFileSuite(
            t, setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))
    return tests

if __name__ == '__main__':
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_autocomplete.settings'
        unittest.main()
