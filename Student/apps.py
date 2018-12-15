# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class StudentConfig(AppConfig):
    name = 'Student'

    def ready(self):
	    import Student.signals
