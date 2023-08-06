# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'xyz_deso'
    label = 'deso'
    verbose_name = 'Deso'

    def ready(self):
        super(Config, self).ready()
