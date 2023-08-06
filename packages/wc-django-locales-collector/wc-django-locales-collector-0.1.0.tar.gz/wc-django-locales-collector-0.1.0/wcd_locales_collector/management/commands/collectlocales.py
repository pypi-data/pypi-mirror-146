from typing import List, Optional
from django.core.management.base import BaseCommand
from wcd_locales_collector.services import collector
from wcd_locales_collector.conf import settings
from logging import getLogger


logger = getLogger(__name__)


class Command(BaseCommand):
    help = 'Collects module locales into a separate folder.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--module', '-m', nargs='+', type=str,
            help='Additional modules to collect from.',
        )
        parser.add_argument(
            '--path', '-p', nargs='?', type=str, default=None,
            help='Change default path to collect translations into.',
        )

    def handle(
        self,
        *args,
        module: List[str] = [],
        path: Optional[str] = None,
        **options
    ):
        result_path = path or settings.PATH

        logger.debug('Result path: %s' % result_path)

        if not result_path:
            self.stdout.write(self.style.ERROR('No path specified.'))
            return

        modules: List[str] = [] + settings.MODULES + (module or [])

        logger.debug('Modules list: %s' % modules)

        if len(modules) < 1:
            self.stdout.write(self.style.ERROR('No modules specified.'))
            return

        collector.collect_locales(
            modules, result_path,
            report_error=lambda *args: self.stdout.write(self.style.WARNING(*args))
        )
