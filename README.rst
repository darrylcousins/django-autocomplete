Django Autocomplete
===================

Autocomplete for django models. Form widgets and admin integration examples.

Requirements
------------

For the widgets bootstrap3 is required django-bootstrap3_ is a good option. To
use the widgets in the admin then bootstrapped3_ admin will be useful.

Installation
------------

Simple install into a virtualenv for testing and evaluation::

    $ git clone https://github.com/darrylcousins/django-autocomplete.git
    $ cd django-autocomplete
    $ python setup.py develop

Other Requirements
------------------

For the extra packages to run flake, sphinx and coverage and to run the test
project django-bootstrap3_ and bootstrapped3_ admin are installed from
requirements.txt.::

    $ pip install -r requirements.txt

Run Tests
---------

Run the tests::

    $ python runtests.py

Run the tests with coverage (needs the extra packages as mentioned above)::

    $ python runtests.py coverage

Build and Run Test Project
--------------------------

Get the test project from github::

    $ git clone https://github.com/darrylcousins/django-project.git
    $ cd django-project
    $ python setup.py develop

The test project uses django-bootstrap3_ and bootstrapped3_ admin.  these extra
packages can be installed with::

    $ pip install -r requirements.txt

The test project has some tests::

    $ python manage.py test project

The tables and sample data can be installed with::

    $ python manage.py migrate
    $ python manage.py loaddata project/fixtures/project.json

And can be run with::

    $ python manage.py runserver 9000

There are no urls beyond the admin screens and api json views. It attempts to
demonstrate the autocomplete widgets.

Setting up models to use autocomplete
-------------------------------------

To set up models to use the autocomplete widgets they need to have a api view
that will return json which is a list of the items filtered by the request
variable `term`, which itself is the default search variable sent with request
by the `jqueryui autocomplete widget <http://jqueryui.com/autocomplete/>`_.

The design decision of this package is to have configuration made at the model level::

    >>> class MyModel(models.Model):
    ...     autocomplete = AutocompleteMeta(
    ...       name=name,
    ...       path='api/filter/mymodel'

The meta model has other attributes that may be set.

Permissions may be set for the autocomplete in three ways. As a boolean, if
true then the request user must be authenticated, if a string then the single
permission is checked, if a list then the user must have all permissions in the
list (see `has_perms
<https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.User.has_perm>`_).

The default is ``None``::

    ...      permissions=True,
    ...      permissions='is_staff',
    ...      permissions=['is_staff'],

The default is to filter on all Char and Text fields but the developer can
define the fields to search on::

    ...      fields=['name', 'description'],

The default behaviour is to also search on searchable fields in the models
related by ForeignKey, but this can be disabled::

    ...      follow_fks=False,
    ...     )


.. note:: setting an attribute `autocomplete` that is an instance of
          `:class:django_autocomplete.meta.Autocomplete` is required for each model
          chosen to use autocomplete widgets.

Urls
----

As can be seen above, each model sets its path to the api view. In order for
these views to be created set the following in `urls.py`::

        url(r'', include('django_autocomplete.urls')),

.. note:: do not use a prefix (e.g. r'api/') as only the path set by
          `MyModel.autocomplete.path` is used.

Once this is done then the view (following the `MyModel` example)
`/api/filter/mymodel/` will be available to the autocomplete widgets::

        http://localhost:8000/api/filter/mymodel/?term=se

The View
--------

The view used to answer the get request is
:class`django_autocomplete.views.AutocompleteView`. This view has its own
``search`` method but the developer can provide a custom search method for the
autocomplete. From the :class`AutocompleteView`::

        // the developer can implement own search method
        if hasattr(self.model.objects, 'search'):
            queryset = self.model.objects.search(
                self.model.objects.all(),
                self.request,
                [term])
        else:
            queryset = self.search(
                self.model.objects.all(),
                [term])

Admin
-----

Formfield widgets
*****************

The only examples found in the example project hooks the widgets into the
bootstrapped3_
admin. To use the widgets all that is required in most cases is to set
`formfield_overrides`::

        class MyModelAdmin(admin.ModelAdmin):
            formfield_overrides = {
              models.ForeignKey: {'widget': AutocompleteSelectWidget},
              models.ManyToManyField: {'widget': AutocompleteSelectMultipleWidget},
              }

Equally so for inlines formsets::

        class MyModelInline(admin.TabularInline):
            formfield_overrides = {
              models.ForeignKey: {'widget': AutocompleteSelectWidget},
              models.ManyToManyField: {'widget': AutocompleteSelectMultipleWidget},
              }

`AutocompleteSelectMultipleWidget` can also be used in reverse many to one
relationships but an admin form will be required. See
`class:project.forms.CountryModelForm` for an example.

.. note:: For inlines the template `admin/inlines/inline_tabular.html` has been
          altered to hook the widgets into the javascript.

Generic Content Type Widget
***************************

There is a autocomplete widget for generic content types. Simplest implementation is as above::

        class TaggedItemAdmin(admin.ModelAdmin):
            model = TaggedItem
            formfield_overrides = {
                models.ForeignKey: {'widget': AutocompleteCTWidget},
                }

But some assumptions are made, namely the ``object_id`` is assumed to be name
``object_id``. More finely grained implementation will use ``formfield_for_foreignkey``::

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.rel.to == ContentType:
                kwargs['widget'] = AutocompleteCTWidget
                kwargs['widget'].object_field = 'object_id'
            return super(TaggedItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

Although untested it should allow for a different name for the ``object_id`` field and for models with more than one ``GenericForeignKey``.

It has not been tested for inline forms but there is an example of usage in `django-project`_.

Changelist Search
*****************

`class:django_autocomplete.widgets.SearchInput` can be used in the
bootstrapped3_ admin list views to provide autocomplete search for autocomplete
enabled models.

This must be explicitly configured in the ModelAdmin::

        class MyModelAdmin(admin.ModelAdmin):
            model = MyModel
            search_form = searchform_factory(MyModel)

..note:: The template `admin/search_form.html` tests for the presence
         `model_admin.search_form` and renders the form if defined.

Using Widgets Outside the Admin
-------------------------------

Each of the widgets need to be aware of the model they are searching. Thus they
have access to the `autocomplete` attribute of the model. The example form
`:model:django_autocomplete.forms.SearchForm` provides and example of setting
up a form to be model aware. It closely follows the django ModelForm to do so.

.. _bootstrapped3: <https://github.com/darrylcousins/django-admin-bootstrapped3>
.. _django-project: <https://github.com/darrylcousins/django-project>
.. _django-bootstrap3: <https://github.com/dyve/django-bootstrap3>
