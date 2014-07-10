# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

from django_autocomplete.widgets import SmallTextareaWidget
from django_autocomplete.widgets import AutocompleteSelectWidget
from django_autocomplete.widgets import AutocompleteSelectMultipleWidget

from .models import Silly
from .models import SillyFK
from .models import SillyM2M

DEFAULT_FORMFIELD_OVERRIDES = {
    models.TextField: {'widget': SmallTextareaWidget},
    models.ForeignKey: {'widget': AutocompleteSelectWidget},
    models.ManyToManyField: {'widget': AutocompleteSelectMultipleWidget},
    }


class SillyInline(admin.TabularInline):
    model = Silly
    extra = 0
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES


class SillyAdmin(admin.ModelAdmin):
    model = Silly
    list_display = ['name']
    search_fields = ['name', ]
    list_editable = ['name', ]
    list_filter = ['name']
    list_per_page = 3
    save_as = True
    save_on_top = True
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES


class SillyFKAdmin(admin.ModelAdmin):
    model = SillyFK
    list_display = ['name']
    search_fields = ['name', ]
    list_editable = ['name', ]
    list_filter = ['name']
    list_per_page = 3
    save_as = True
    save_on_top = True
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES
    inlines = [
        SillyInline,
        ]


class SillyM2MAdmin(admin.ModelAdmin):
    model = SillyM2M
    list_display = ['name']
    search_fields = ['name', ]
    list_editable = ['name', ]
    list_filter = ['name']
    list_per_page = 3
    save_as = True
    save_on_top = True
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES


# Register your models here.
admin.site.register(Silly, SillyAdmin)
admin.site.register(SillyFK, SillyFKAdmin)
admin.site.register(SillyM2M, SillyM2MAdmin)
