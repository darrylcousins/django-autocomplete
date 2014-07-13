# -*- coding: utf-8 -*-
from django import forms
from django.forms import BaseForm
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.models import ModelFormOptions
from django.utils.six import with_metaclass

from .widgets import SearchInput


class SearchFormMetaclass(DeclarativeFieldsMetaclass):
    """
    The search form meta class ensures the form has a model.
    """
    def __new__(mcs, name, bases, attrs):
        new_class = super(SearchFormMetaclass, mcs).__new__(mcs, name, bases, attrs)
        new_class.opts = new_class._meta = ModelFormOptions(getattr(new_class, 'Meta', None))

        # here the purpose for the meta class - to assign model to the widget
        new_class.base_fields['q'] = forms.CharField(widget=SearchInput(model=new_class.opts.model))

        return new_class


class SearchForm(with_metaclass(SearchFormMetaclass, BaseForm)):
    """
    A simple search form which used the autocomplete SearchInput widget.
    """
    q = forms.CharField(widget=SearchInput)

    class Meta:
        model = None

    def __init__(self, **kwargs):
        opts = self._meta
        if opts.model is None:
            raise ValueError('SearchForm has no model class specified.')
        super(SearchForm, self).__init__(**kwargs)


def searchform_factory(model, form=SearchForm):
    """
    Returns a SearchForm - in essence from django.forms.models.modelform_factory

    """
    # Build up a list of attributes that the Meta object will have.
    attrs = {'model': model}

    # If parent form class already has an inner Meta, the Meta we're
    # creating needs to inherit from the parent's inner meta.
    parent = (object,)
    if hasattr(form, 'Meta'):
        parent = (form.Meta, object)
    Meta = type(str('Meta'), parent, attrs)

    # Give this new form class a reasonable name.
    class_name = model.__name__ + str('SearchForm')

    # Class attributes for the new form class.
    form_class_attrs = {
        'Meta': Meta,
    }

    # Instatiate type(form) in order to use the same metaclass as form.
    return type(form)(class_name, (form,), form_class_attrs)
