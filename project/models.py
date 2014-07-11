# -*- coding: utf-8 -*-
from django.db import models

from django_autocomplete.meta import AutocompleteMeta


API_FILTER_PATH = 'api/filter'


def get_autocomplete_meta(name):
    return AutocompleteMeta(
        name=name,
        path='%s/%s' % (API_FILTER_PATH, name)
        )


class Timestamped(models.Model):
    """
    The Timestamped model, all models in the application share its attributes.

        >>> obj = Timestamped()
        >>> obj.created

    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Base(models.Model):
    """
    The Base model, all models in the application share its attributes.

        >>> obj = Base(name='base')
        >>> obj.name
        'base'

    """
    name = models.CharField(
        max_length=30
        )

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.name)

    def __str__(self):
        return '%s' % (self.name)


class Country(Base, Timestamped):
    """
    The Country model. Each town has a ForeignKey to its Country.

        >>> obj = Country.objects.create(name='usa')
        >>> obj.autocomplete.name
        'country'
        >>> obj.autocomplete.path
        'api/filter/country'

        >>> obj.delete()

    """
    autocomplete = get_autocomplete_meta('country')

    class Meta:
        verbose_name_plural = 'Countries'


class Organisation(Base, Timestamped):
    """
    The Organisation model. It has a many to many relationship with Towns.

        >>> obj = Organisation.objects.create(name='microsoft')
        >>> obj.autocomplete.name
        'organisation'
        >>> obj.autocomplete.path
        'api/filter/organisation'

        >>> obj.delete()

    """
    autocomplete = AutocompleteMeta(
        name='organisation',
        path='%s/organisation' % API_FILTER_PATH
        )


class Town(Base, Timestamped):
    """
    The Town model.

        >>> usa = Country.objects.create(name='usa')
        >>> obj = Town.objects.create(name='redmond', country=usa)
        >>> obj.autocomplete.name
        'town'
        >>> obj.autocomplete.path
        'api/filter/town'

    Has a country:

        >>> obj.country
        <Country: usa>

    Has organisations:

        >>> obj.organisations.all()
        []

    Can have sister towns:

        >>> obj.sister_towns.add(Town.objects.create(name='redmond', country=usa))
        >>> obj.sister_towns.all()
        [<Town: redmond>]

    Clean up

        >>> usa.delete()
        >>> obj.delete()

    """
    country = models.ForeignKey(Country)
    organisations = models.ManyToManyField(
        Organisation,
        through='project.OrganisationTown',
        related_name='towns'
        )
    sister_towns = models.ManyToManyField('self', blank=True)

    autocomplete = AutocompleteMeta(
        name='town',
        path='%s/town' % API_FILTER_PATH
        )


class OrganisationTown(Timestamped):
    """
    The OrganisationTown model. It is the `through` model for Towns and
    Organisations.

        >>> usa = Country.objects.create(name='usa')
        >>> town = Town.objects.create(name='redmond', country=usa)
        >>> org = Organisation.objects.create(name='microsoft')

    Join them with the through table:

        >>> import datetime
        >>> join = OrganisationTown.objects.create(
        ...     joined=datetime.date(2014, 7, 10), town=town,
        ...     organisation=org)

    Clean up

        >>> usa.delete()
        >>> town.delete()
        >>> org.delete()
        >>> join.delete()

    """
    organisation = models.ForeignKey(Organisation)
    town = models.ForeignKey(Town)
    joined = models.DateField()

    autocomplete = AutocompleteMeta(
        name='organisationtown',
        path='%s/organisationtown' % API_FILTER_PATH
        )

    class Meta:
        verbose_name = 'Organisation Town Join'


