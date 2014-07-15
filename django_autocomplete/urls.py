# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.conf.urls import url
from django.db import models

from .meta import AutocompleteMeta
from .views import AutocompleteView


def make_api_urls(_urlpatterns, model):
    """
    Helper method to generate API urls.

        >>> from django_autocomplete.urls import make_api_urls
        >>> make_api_urls([], TestModel)
        [<RegexURLPattern autocomplete_view_silly ^api/filter/silly/$>]

    This can be used from project urls and will create autocomplete urls from
    any model that has an autocomplete attribute that is an instance of
    :class:`django_autocomplete.meta.AutocompleteMeta`.

    For example::

        url(r'', include('django_autocomplete.urls')),

    .. note:: no prefix should be added because it is expected that the path to
        the autocomplete url for a model is defined at model level.

    """
    _urlpatterns.append(
        url(r'^%s$' % (
            model.autocomplete.path
            ),
            AutocompleteView.as_view(
                model=model,
                ),
            name='autocomplete_view_%s' % (model.autocomplete.name)),
        )
    return _urlpatterns

urlpatterns = ['']
for model in models.get_models(include_auto_created=False):
    if hasattr(model, 'autocomplete') and isinstance(model.autocomplete, AutocompleteMeta):
        urlpatterns = make_api_urls(urlpatterns, model)

urlpatterns = patterns(*urlpatterns)
