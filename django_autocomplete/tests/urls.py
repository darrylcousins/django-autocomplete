# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    # the models must define path to autocomplete view
    url(r'', include('django_autocomplete.urls')),
    )

