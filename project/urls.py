# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # the models must define path to autocomplete view
    url(r'^api/', include('django_autocomplete.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    )

urlpatterns = patterns(*urlpatterns)
