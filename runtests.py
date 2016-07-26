#!/usr/bin/env python
import sys
import os
import warnings

from django.conf import settings
from django.core.management import execute_from_command_line


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'cache_extension',
            'tests',
        ],
        CACHES={
            "default": {
                'NAME': '17bdc',
                'BACKEND': 'cache_extension.backends.redis.ExtensionRedisBackend',
                'LOCATION': 'redis://localhost:6379/0',
                'TIMEOUT': '172800',
                "KEY_PREFIX": "cache_extension",
                'OPTIONS': {
                    "DB": 0,
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    'PARSER_CLASS': 'redis.connection.HiredisParser',
                    'PICKLE_VERSION': 2,
                }
            }
        },

        MIDDLEWARE_CLASSES=[],
    )


warnings.simplefilter('default', DeprecationWarning)
warnings.simplefilter('default', PendingDeprecationWarning)


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
