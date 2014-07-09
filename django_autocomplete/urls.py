# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.db import models
from django.conf import settings

from .views import AutocompleteView

def make_api_urls(_urlpatterns, model):
    """
    Helper method to generate API urls.
    """
    _urlpatterns.append(
        url(r'^%s/$' % (
            model.autocomplete.path
            ),
            AutocompleteView.as_view(
                model=model,
                ),
            name='%s_api_%s' % (model._meta.db_name, query)),
        )
    return urlpatterns

urlpatterns = ['']

for model in models.get_models(include_auto_created=True):
    if hasattr(model, 'autocomplete'):
        urlpatterns = make_api_urls(urlpatterns, model)

urlpatterns = patterns(*urlpatterns)

