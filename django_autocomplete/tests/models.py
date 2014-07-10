# -*- coding: utf-8 -*-
from django.db import models

from django_autocomplete.meta import AutocompleteMeta


class TestFKModel(models.Model):
    app_label = 'django_autocomplete'
    model_name = 'testfkmodel'

    name = models.CharField(max_length=30)
    description = models.TextField()


class TestModel(models.Model):
    app_label = 'django_autocomplete'
    model_name = 'testmodel'

    name = models.CharField(max_length=30)
    description = models.TextField()
    fkm = models.ForeignKey(TestFKModel, null=True)
    fkms = models.ManyToManyField(
        TestFKModel,
        related_name="tms",
        null=True)

    autocomplete = AutocompleteMeta(
        name='silly',
        path='api/filter/silly',
        )
