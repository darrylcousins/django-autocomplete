# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

from django_autocomplete.widgets import SmallTextareaWidget
from django_autocomplete.widgets import AutocompleteSelectWidget
from django_autocomplete.widgets import AutocompleteSelectMultipleWidget
from django_autocomplete.forms import searchform_factory

from .models import Town
from .models import Country
from .models import Organisation
from .models import OrganisationTown


DEFAULT_FORMFIELD_OVERRIDES = {
    models.TextField: {'widget': SmallTextareaWidget},
    models.ForeignKey: {'widget': AutocompleteSelectWidget},
    models.ManyToManyField: {'widget': AutocompleteSelectMultipleWidget},
    }


class BaseInline(admin.TabularInline):
    extra = 0
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES


class TownInline(BaseInline):
    model = Town
    fields = ['name']


class OrganisationTownInline(BaseInline):
    model = OrganisationTown
    verbose_name = 'Organisation'
    verbose_name_plural = '%ss' % verbose_name


class TownOrganisationInline(BaseInline):
    model = OrganisationTown
    verbose_name = 'Town'
    verbose_name_plural = '%ss' % verbose_name


class CountryInline(BaseInline):
    model = Country


class BaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'modified']
    search_fields = ['name']
    list_editable = ['name']
    list_per_page = 2
    save_as = True
    date_hierarchy = 'created'
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES


class TownAdmin(BaseAdmin):
    model = Town
    search_form = searchform_factory(Town)
    inlines = [
        OrganisationTownInline,
        ]


class CountryAdmin(BaseAdmin):
    model = Country
    search_form = searchform_factory(Country)
    inlines = [
        TownInline,
        ]


class OrganisationAdmin(BaseAdmin):
    model = Organisation
    search_form = searchform_factory(Organisation)
    inlines = [
        TownOrganisationInline,
        ]


class OrganisationTownAdmin(admin.ModelAdmin):
    model = OrganisationTown
    list_display = ['created', 'modified']
    list_per_page = 2
    save_as = True
    date_hierarchy = 'created'
    search_form = searchform_factory(OrganisationTown)


# Register your models here.
admin.site.register(Town, TownAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(OrganisationTown, OrganisationTownAdmin)
