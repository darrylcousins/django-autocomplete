# -*- coding: utf-8 -*-


class AutocompleteMeta:
    """
    Simple meta class to allow the model to define aspects of the autocomplete.

    :var name: used for the named url
    :var path: the path to autocomplete view
    :var follow_fks: when searching should ForeignKey fields be followed.
    :var fields: list of fields, if empty then all searchable fields are used
    :var permissions: bool, string or iter

    * if ``permissions`` ``False`` (default) no authentication is checked.
    * if ``permissions`` ``True`` then request.user must be authenticated.
    * if ``permissions`` ``string`` then request.user must have the permission defined by ``string``.
    * if ``permissions`` ``iter`` then request.user must have all the permissionis defined in the ``iter``

    See :class:`django_autocomplete.views.AutocompleteView` for more clarification.

    For example as a simple object:

        >>> from django_autocomplete.meta import AutocompleteMeta
        >>> class TestModel(object):
        ...     autocomplete = AutocompleteMeta(
        ...         name='silly',
        ...         path='api/filter/silly',
        ...         )


    The model autocomplete configures the model for use:

        >>> m = TestModel()
        >>> m.autocomplete
        <django_autocomplete.meta.AutocompleteMeta object at 0x...>

        >>> m.autocomplete.path
        'api/filter/silly'
        >>> m.autocomplete.name
        'silly'
        >>> m.autocomplete.follow_fks
        True
        >>> m.autocomplete.fields
        []

    """
    name = ''
    path = ''
    fields = []
    permissions = None
    follow_fks = True

    def __init__(self, autocomplete=None, **kwargs):
        if autocomplete:
            autocomplete_attrs = autocomplete.__dict__
        else:
            autocomplete_attrs = kwargs
        for attr in self.__class__.__dict__:
            if attr in autocomplete_attrs:
                self.__dict__[attr] = autocomplete_attrs[attr]


