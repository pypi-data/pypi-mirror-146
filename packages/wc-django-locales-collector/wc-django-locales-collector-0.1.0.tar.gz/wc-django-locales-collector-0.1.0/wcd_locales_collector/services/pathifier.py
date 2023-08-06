from typing import List, Optional
import os
import inspect
from importlib import import_module


__all__ = (
    'get_path', 'get_module_path',
    'get_module_result_path', 'get_modules_result_paths',
)

LOCALES_PATH_FORMAT = '{path}/locale/'


def get_path(module: str) -> Optional[str]:
    try:
        md = import_module(module)
    except ImportError:
        return None

    return os.path.dirname(inspect.getfile(md))


def get_module_path(module: str) -> Optional[str]:
    path = get_path(module)

    if path is None:
        return None

    return LOCALES_PATH_FORMAT.format(path=path)


def get_module_result_path(module: str, base_path: str) -> Optional[str]:
    return os.path.join(base_path, module.replace('.', '_'))


def get_modules_result_paths(modules: List[str], base_path: str) -> List[str]:
    return [get_module_result_path(module, base_path) for module in modules]
