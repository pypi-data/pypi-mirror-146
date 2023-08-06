from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from .discovery import autodiscover


__all__ = ('LocalesCollectorConfig',)


class LocalesCollectorConfig(AppConfig):
    name = 'wcd_locales_collector'
    verbose_name = pgettext_lazy('wcd_locales_collector', 'Locales collector')

    def ready(self):
        autodiscover()
