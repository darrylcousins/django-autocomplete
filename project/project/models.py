# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Silly(models.Model):
    """
    The Silly model.

        >>> silly = Silly.objects.create(name='silly')

    Has an autocomplete path.

        >>> silly.autocomplete

    """
    name = models.TextField()

    @classproperty
    def autocomplete(self):
        """
        Marks the model has having autocomplete.
        """
        return dict(
            path='api/filter/silly'
            )
