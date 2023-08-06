from dataclasses import dataclass, field
from typing import List, Optional
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


@s('WCD_LOCALES_COLLECTOR')
@dataclass
class Settings:
    """
    Example:

    ```python
    WCD_LOCALES_COLLECTOR = {
        "MODULES": [],
    }
    ```
    """
    PATH: Optional[str] = None
    MODULES: List[str] = field(default_factory=list)


settings = Settings()
