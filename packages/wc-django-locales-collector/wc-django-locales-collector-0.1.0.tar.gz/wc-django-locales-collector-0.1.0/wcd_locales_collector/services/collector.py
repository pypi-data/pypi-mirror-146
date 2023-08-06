from typing import List
import os
from django.core.management.utils import popen_wrapper
from logging import getLogger

from . import pathifier


__all__ = 'collect_locales',

logger = getLogger(__name__)


MSGMERGE_DEFAULT_ARGS = [
    'msgmerge', '-q', '--previous',
]
MSGCAT_DEFAULT_ARGS = [
    'msgcat', '--use-first',
]


def merge(path_from: str, path_to: str):
    os.makedirs(os.path.dirname(path_to), exist_ok=True)
    # If no file exists - create blank.
    open(path_to, 'a').close()

    # Merging all source new occurences.
    r = popen_wrapper(
        MSGMERGE_DEFAULT_ARGS + [path_to, path_from, '-o', path_to],
    )

    if r[2] != 0:
        return r

    # Merging filled source data to an empty new.
    return popen_wrapper(
        MSGCAT_DEFAULT_ARGS + [path_to, path_from, '-o', path_to],
    )


def collect_locales(
    modules: List[str],
    result_path: str,
    report_error: lambda *args: logger.warning(*args)
):
    result_path = os.path.abspath(result_path)

    for module in modules:
        path = pathifier.get_module_path(module)

        if not path:
            logger.warning('Module %s not found.' % module)
            continue

        module_path = pathifier.get_module_result_path(module, result_path)

        for root, dirs, files in os.walk(path):
            dir = os.path.join(module_path, root.replace(path, ''))

            for file in files:
                if file.endswith('.po'):
                    file_path = os.path.join(root, file)
                    new_path = os.path.join(dir, file)

                    _, errors, status = merge(file_path, new_path)

                    if status != 0:
                        report_error(errors)
