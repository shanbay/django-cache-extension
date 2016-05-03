=====
Django cache extension
=====


Quick start
-----------

1. Install ``cache extension`` by pip::

    pip install django-cache-extension

2. For redis backend use cache like this::

    config your cache file backend to cache_extension:

    CACHES={
          "default": {
              'BACKEND': 'cache_extension.backends.redis.ExtensionRedisBackend',
              'LOCATION': 'redis://redis:6379/0',
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
