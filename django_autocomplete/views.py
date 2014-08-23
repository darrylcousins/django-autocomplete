# -*- coding: utf-8 -*-
import json

from django.db import models
from django.http import HttpResponse
from django.views.generic import View


class AutocompleteView(View):
    """
    Simple json response view as backend support to the autocomplete form.

        >>> view = AutocompleteView.as_view(model=TestModel)

    """
    model = None
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """
        Returns the dict response that will be serialized and returned:

            >>> view = AutocompleteView()
            >>> view.model = TestModel
            >>> request = request_factory.get('/')
            >>> request.GET = {'term': 'blood'}
            >>> response = view.get(request)
            >>> response.status_code
            200
            >>> response.content
            b'[]'

        We can set permissions to ``True`` that the request user should be
        authenticated.

            >>> m = TestModel()
            >>> m.autocomplete.permissions = True
            >>> view.model = m

        Create a user::

            >>> user = User.objects.create_user('member', password='member')
            >>> user.save()

        Unauthenticated user::

            >>> client = Client()
            >>> response = client.get('/api/filter/silly/?term=c')
            >>> response.status_code
            401

        Authenticate::

            >>> client.login(username='member', password='member')
            True
            >>> response = client.get('/api/filter/silly/?term=c')
            >>> response.status_code
            200

        Say we have a permission we want for our users::

            >>> m.autocomplete.permissions = 'is_staff'
            >>> view.model = m
            >>> response = client.get('/api/filter/silly/?term=c')
            >>> response.status_code
            401

        Create a staff user and try again::

            >>> admin = User.objects.create_superuser('admin', email='admin@admin.org', password='admin')
            >>> admin.save()
            >>> client.login(username='admin', password='admin')
            True
            >>> response = client.get('/api/filter/silly/?term=c')
            >>> response.status_code
            200

        Permissions can be a list too::

            >>> m.autocomplete.permissions = ['is_staff', 'is_superuser']
            >>> view.model = m
            >>> response = client.get('/api/filter/silly/?term=c')
            >>> response.status_code
            200

        """
        self.request = request
        perms = self.model.autocomplete.permissions
        if perms is not None:
            if not request.user.is_authenticated():
                return HttpResponse('Unauthorized', status=401)
            if not isinstance(perms, bool):
                if isinstance(perms, bytes):
                    perms = [perms]
                if not request.user.has_perms(perms):
                    return HttpResponse('Unauthorized', status=401)
        # passed permissions
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Returns the dict response that will be serialized and returned:

            >>> view = AutocompleteView()
            >>> view.model = TestModel
            >>> request = request_factory.get('/')
            >>> request.GET = {'term': 'blood'}
            >>> view.request = request

            >>> context = view.get_context_data()
            >>> print(context)
            []

        With the appropiate object in db it finds something to return.

            >>> m = TestModel(name='Silly model',
            ...     description='Dumb description')
            >>> m.save()
            >>> request.GET = {'term': 'silly'}
            >>> view.request = request
            >>> context = view.get_context_data()
            >>> len(context)
            1
            >>> context[0]['label']
            'Silly model'

        All searchable fields are searched, e.g. the description here:

            >>> request.GET = {'term': 'dumb'}
            >>> view.request = request
            >>> context = view.get_context_data()
            >>> len(context)
            1
            >>> context[0]['label']
            'Silly model'

        Clean up.

            >>> m.delete()

        """
        term = self.request.GET.get('term')
        context = []
        if not term:
            return context

        queryset = self.search(
            self.model.objects.all(),
            [term])

        for item in queryset.all():
            context.append(dict(
                id=item.pk,
                value=str(item),
                label=str(item)
                ))
        return context

    def render_to_json_response(self, context, **response_kwargs):
        """
        Does the work to convert context data and return json response.

            >>> view = AutocompleteView()
            >>> view.model = TestModel
            >>> context = [{'id': 1, 'label': 'My marker', 'value': 'My marker'}]
            >>> response = view.render_to_response(context)
            >>> response.status_code
            200

        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
            )

    def convert_context_to_json(self, context):
        """
        Does the work to convert context data to json.

            >>> view = AutocompleteView()
            >>> context = [{'id': 1, 'label': 'My marker', 'value': 'My marker'}]
            >>> keys = view.convert_context_to_json(context)
            >>> keys = list(context[0].keys())
            >>> keys.sort()
            >>> print(keys)
            ['id', 'label', 'value']

        Yes, looks the same, trust me, it is json.

        """
        return json.dumps(context)

    def render_to_response(self, context, **response_kwargs):
        """
        Override :class:`django.views.generic.base.View` to return json response.
        """
        return self.render_to_json_response(context, **response_kwargs)

    def is_searchable_field(self, field):
        """
        """
        if isinstance(field, models.TextField) or isinstance(field, models.CharField):
            return True
        return False

    def search(self, queryset, terms):
        """
        Search method. This can be overridden by giving the model manager a ``search`` method.

        :arg queryset: :class:`django.db.models.QuerySet`
        :arg terms:    :list: of strings
        :returns:      the filtered :class:`django.db.modesls.QuerySet`

        Searches all text fields

           >>> m = TestModel(name='My silly model',
           ...     description='a cool description')
           >>> m.save()

           >>> manager = TestModel.objects
           >>> queryset = manager.all()

        Verify that we have objects to search on::

           >>> queryset
           [<TestModel: TestModel object>]

        Try a term that will fail::

           >>> view = AutocompleteView()
           >>> view.model = TestModel
           >>> view.search(queryset, ['empty'])
           []

        And a term that will return::

           >>> view.search(queryset, ['cool'])
           [<TestModel: TestModel object>]


        The model has a ``autocomplete`` attribute that is an instance of 
        :class:`django_autocomplete.meta.AutocompleteMeta`. The test model
        allows ForeignKey fields to be followed.

        Try a term that will follow the foreign key field and search in the related object::

            >>> fkm = TestFKModel(name='My nice company',
            ...     description='a nice description')
            >>> fkm.save()
            >>> m.fkm = fkm
            >>> m.save()
            >>> view.search(queryset, ['nice'])
            [<TestModel: TestModel object>]

        Clean up.

            >>> m.delete()
            >>> fkm.delete()

        """
        q = None
        for term in terms:
            if not isinstance(term, str):
                raise TypeError("search terms must be a string or list of strings, "
                                "not '%s'." % term.__class__.__name__)
            term = term.encode('utf-8')
            # search all possible fields
            if self.model.autocomplete.fields:
                fields = self.model.autocomplete.fields
            else:
                fields = self.model._meta.fields
            q = self._construct_q(
                q, fields, term,
                follow_fks=self.model.autocomplete.follow_fks
                )

        return queryset.filter(q)

    def _construct_q(self, q, fields, term, follow_fks=True):
        """
        Constructs a query following foreign key fields.

        :arg q:      :class:`django.db.models.Q` object
        :arg fields: :list: django model fields
        :arg term:   :str: search term
        :returns:    :class:`django.db.models.Q` object

        Get the object manaager for an object that has fk fields.

            >>> view = AutocompleteView()
            >>> view.model = TestModel

        Get the fields and check:

            >>> fields = TestModel._meta.fields
            >>> [field.name for field in fields]
            ['id', 'name', 'description', 'fkm']

        Construct a query that spans all three objects:

            >>> q = view._construct_q(None, fields, 'silly_search', follow_fks=True)

        The query is an *OR* query:

            >>> print(q)
            (OR: (...))

            >>> print('\\n'.join([str(child) for child in q.children]))
            ('name__icontains', 'silly_search')
            ('description__icontains', 'silly_search')
            ('fkm__name__icontains', 'silly_search')
            ('fkm__description__icontains', 'silly_search')

        The method will also accept a list of field names and will look up the field by name:

            >>> fields = ['name']
            >>> q = view._construct_q(None, fields, 'silly_search', follow_fks=False)
            >>> print('\\n'.join([str(child) for child in q.children]))
            ('name__icontains', 'silly_search')

        Unacceptable fields raise error:

            >>> fields = ['nofield']
            >>> q = view._construct_q(None, fields, 'silly_search', follow_fks=False)
            Traceback (most recent call last):
            ...
            django.db.models.fields.FieldDoesNotExist: TestModel has no field named 'nofield'


        """
        for field in fields:
            # may be passed a list of field names
            if not isinstance(field, models.fields.Field):
                field = self.model._meta.get_field_by_name(field)[0]
            is_fk = isinstance(field, models.ForeignKey)
            if self.is_searchable_field(field) and not is_fk:
                kwargs = {'%s__icontains' % field.name: term}
                q = self._start_query(q, **kwargs)
            elif is_fk and follow_fks:
                for ifield in field.rel.to._meta.fields:
                    if self.is_searchable_field(ifield):
                        kwargs = {'%s__%s__icontains' % (field.name, ifield.name): term}
                        q = self._start_query(q, **kwargs)
        return q

    def _start_query(self, q, **kwargs):
        """
        Helper method to ensure the validity of the Q objects in the chain of ``OR`` queries

        :arg q:        :class:`django.db.models.Q` object or None
        :arg kwargs: :dict: ``field name`` ``search term`` values
        :returns:      :class:`django.db.models.Q` object

        Something like:

            >>> view = AutocompleteView()
            >>> q = view._start_query(None, filter="filter")
            >>> q = view._start_query(q, name="name")
            >>> print(q)
            (OR: ('filter', 'filter'), ('name', 'name'))

        """
        if not q:
            q = models.Q(**kwargs)
        else:
            q = q | models.Q(**kwargs)
        return q

