import os
import sys
from importlib import import_module

ENVIRONMENT = os.environ.get("DJANGO_ENV", "development")

settings_module = f"proj.settings.{ENVIRONMENT}"
try:
    settings = import_module(settings_module)
except ImportError:
    raise ImportError(f"Could not import settings '{settings_module}'")

# Expose all settings from the imported module
for setting in dir(settings):
    if setting.isupper():
        setattr(sys.modules[__name__], setting, getattr(settings, setting))
