Django Autocomplete
===================

Autocomplete for django models. Form widgets and admin integration examples.

Requirements
------------

For the widgets bootstrap3 is required
`django-bootstrap3<https://github.com/dyve/django-bootstrap3.git>` is a good
option. To use the widgets in the admin then
'django-admin-bootstrap3<https://github.com/darrylcousins/django-admin-bootstrapped3>'
will be useful.

Installation
------------

Simple install into a virtualenv for testing and evaluation::

    $ git clone https://github.com/darrylcousins/django-autocomplete.git
    $ cd django-autocomplete
    $ python setup.py develop

Other Requirements
------------------

For the extra packages to run flake, sphinx and coverage and to run the test
project django-bootstrap3 and django-admin-bootstrapped3 are installed from
requirements.txt.

    $ pip install -r requirements.txt

Run Tests
---------

Run the tests::

    $ python runtests.py

Run the tests with coverage (needs the extra packages as mentioned above)::

    $ python runtests.py coverage

Run Test Project
----------------

The test project has some tests::

    $ python project/manage.py test project

And can be run::

    $ python project/manage.py runserver 9000
