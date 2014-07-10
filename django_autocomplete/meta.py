# -*- coding: utf-8 -*-


class AutocompleteMeta(object):
    """
    Simple meta class to allow the model to define aspects of the autocomplete.

    :var name: used for the named url
    :var path: the path to autocomplete view
    :var follow_fks: when searching should ForeignKey fields be followed.
    :var fields: list of fields, if empty then all searchable fields are used

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
    follow_fks = True

    def __init__(self, name, path, fields=[], follow_fks=True):
        self.name = name
        self.path = path
        self.fields = fields
        self.follow_fks = follow_fks



