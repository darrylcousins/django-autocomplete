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

Get the test project from github:

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

The meta model has two other attributes that may be set::

    ...      fields=['name', 'description'],

The default is to filter on all Char and Text fields, the second is::

    ...      follow_fks=False,
    ...     )

The default is `True` and the filter will also search on searchable fields in
the fk models.

.. note:: setting an attribute `autocomplete` that is an instance of
          `:model:django_autocomplete.meta.Autocomplete` is required for each model
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

.. warning:: Only TabularInline formsets have been implemented and tested in 
            `django-admin-bootstrapped3 <https://github.com/darrylcousins/django-admin-bootstrapped3>`_,

`AutocompleteSelectMultipleWidget` can also be used in reverse many to one
relationships but an admin form will be required. See
`class:project.forms.CountryModelForm` for an example.

.. note:: For inlines the template `admin/inlines/inline_tabular.html` has been
          altered to hook the widgets into the javascript.

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
.. _django-bootstrap3: <https://github.com/dyve/django-bootstrap3>
