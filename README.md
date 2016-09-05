=====
Django cache extension
=====

[![Build Status](https://travis-ci.org/shanbay/django-cache-extension.svg?branch=master)](https://travis-ci.org/shanbay/django-cache-extension)

Add extension methods to cache

Quick start
-----------

1. Install ``cache extension`` by pip::

    pip install django-cache-extension

2. For redis backend use cache like this::

    config your cache file backend to cache_extension:

    ```
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
    ```

3. For custom cache backend:: 

   ```
   from cache_extension.cache import ExtensionCache
   from some_module import CustomCache
   class ExtensionCustomCache(ExtensionCache, CustomCache):
       pass
   ```


4. Use extension cache methods:: 

   ```
   cache.get_model(Article, pk=1)
   cache.get_models(Article, [1,2,3])
   cache.get_model(UserArticle, user_id=1, article_id=1)
   cache.get_model_list(UserArticle, user_id=1)
   ```

5. Built in cached fields: ForeignKeyField, OneToOneField. Say you have two models defined as below:

    ```
    from django.db import models
    from cache_extension import cached_fields


    class Foo(models.Model):
        pass

    class Bar(models.Model):
        foo = cached_fields.ForeignKeyField(Foo)

    ```

    Then instances of Bar will have a `cached_foo` property which will try to fetch foo from cache first, if cache misses, will fallback to database.
    ```
    bar = Bar.objects.get(pk=1)
    bar.cached_foo # cached foreign field, really handy
    ```

