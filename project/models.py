# -*- coding: utf-8 -*-
from django.db import models

from django_autocomplete.meta import AutocompleteMeta


class SillyFK(models.Model):
    """
    The Silly FK model.
    """
    name = models.TextField()

    autocomplete = AutocompleteMeta(
        name='silly',
        path='api/filter/sillyfk',
        )


class SillyM2M(models.Model):
    """
    The Silly M2M model.
    """
    name = models.TextField()

    autocomplete = AutocompleteMeta(
        name='silly',
        path='api/filter/sillym2m',
        )


class Silly(models.Model):
    """
    The Silly model.

        >>> silly = Silly.objects.create(name='silly')

    Has an autocomplete path.

        >>> silly.autocomplete
        <django_autocomplete.meta.AutocompleteMeta object at 0x...>

    """
    name = models.TextField()
    sillyfk = models.ForeignKey(SillyFK)
    sillym2m = models.ManyToManyField(SillyM2M)

    autocomplete = AutocompleteMeta(
        name='silly',
        path='api/filter/silly',
        )
