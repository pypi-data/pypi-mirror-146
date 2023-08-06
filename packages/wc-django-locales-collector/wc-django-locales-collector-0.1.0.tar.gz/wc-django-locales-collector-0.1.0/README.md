# WebCase locales collector

Collects locales from any python third parties to some local folder. It's useful for a more easier local translations management.

## Installation

```sh
pip install wc-django-locales-collector
```

In `settings.py`:

```python

INSTALLED_APPS += [
  'wcd_locales_collector',
]

WCD_LOCALES_COLLECTOR = {
  # List of modules for which locales will be collected.
  'MODULES': [
    # For example:
    'rest_framework',
  ],
  # Path to save collected locales.
  'PATH' = BASE_ROOT / 'exported_locale'
}

# All root options could also be provided as standalone ones(for overriding, etc.):
WCD_LOCALES_COLLECTOR_PATH = BASE_ROOT / 'replaced_locale'

# ...

# Your static `LOCALE_PATHS` config should be wrapped by paths extender.
# If it's not, then all exported locales will not be applied.
from wcd_locales_collector.helpers import locale_paths_extender

LOCALE_PATHS = locale_paths_extender(LOCALE_PATHS)

# OR!
# If you have some issues with that approach - you can extend `LOCALE_PATHS`
# manually:
from wcd_locales_collector.services import pathifier

LOCALE_PATHS = LOCALE_PATHS + pathifier.get_modules_result_paths(
  WCD_LOCALES_COLLECTOR['MODULES'], WCD_LOCALES_COLLECTOR_PATH
)
```

## Usage

```python
python manage.py collectlocales
```

That's it. You have collected all locales from all provided apps into a separate folder.
