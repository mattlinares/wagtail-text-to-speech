#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import AppConfig


class AltGeneratorAppConfig(AppConfig):
    name = "wagtail_text_to_speech"
    verbose_name = "Alt generator"

    def ready(self):
        import wagtail_text_to_speech.signals  # NOQA
