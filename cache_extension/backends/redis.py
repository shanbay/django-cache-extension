from __future__ import absolute_import

from cache_extension.cache import ExtensionCache

from django_redis.cache import RedisCache, omit_exception
from django_redis.client.default import _main_exceptions
from django_redis.exceptions import ConnectionInterrupted
from redis.exceptions import ResponseError


# use it in setting_conf/caches.py
class ExtensionRedisBackend(ExtensionCache, RedisCache):

    @omit_exception
    def incr(self, key, delta=1, version=None, client=None):

        if not client:
            client = self.client.get_client(write=True)

        key = self.make_key(key, version=version)

        try:
            try:
                value = client.incr(key, delta)
            except ResponseError:
                # if cached value or total value is greater than 64 bit signed
                # integer.
                # elif int is encoded. so redis sees the data as string.
                # In this situations redis will throw ResponseError

                # try to keep TTL of key
                timeout = client.ttl(key)
                value = self.get(key, version=version, client=client) + delta
                self.set(key, value, version=version, timeout=timeout,
                         client=client)
        except _main_exceptions as e:
            raise ConnectionInterrupted(connection=client, parent=e)

        return value
