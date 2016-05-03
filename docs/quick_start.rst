Quick Start
===========

config
-------
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


methods
-------

.. method:: get_model(model, pk=None, cache_exc=False, **kwargs)

    Return django model in cache, query database when cache miss hit, raise Model.DoesNotExist when miss database.

    Set cache_exc=True where cache model.DoesNotExist in cache, and return None.


.. method:: get_model_list(model, **kwargs)

    Get multiple models with filter on fields, return a list of models.

.. method:: clear_model(model, *args)

    clear model cache on args, usually use id.

.. method:: clear_model_list(model, *agrs)

    Clear model cache using field name.

.. method:: clear_model_cache(model, *agrs, **kwargs)

    Call clear_model or clear_model_list dynamically according to params passed.
