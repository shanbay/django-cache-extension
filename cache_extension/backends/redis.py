from __future__ import absolute_import
from cache_extension.cache import ExtensionCache
from django_redis.cache import RedisCache, omit_exception
from django_redis.client.default import _main_exceptions, DefaultClient
from django_redis.exceptions import ConnectionInterrupted
from redis.client import StrictPipeline
from redis.exceptions import ResponseError

KEY_CMDS = ['exists', 'expire', 'expireat', 'rename', 'ttl']
SET_CMDS = ['sadd', 'scard', 'sismember', 'smembers', 'spop', 'srem']
ZSET_CMDS = [
    'zadd', 'zcard', 'zcount', 'zincrby', 'zrange', 'zrem',
    'zrevrange', 'zscore'
]

SUPPORT_CMDS = KEY_CMDS + SET_CMDS + ZSET_CMDS


class ExtensionPipeline(StrictPipeline):
    def __init__(self, connection_pool, response_callbacks, transaction,
                 shard_hint, make_key_func):
        super(ExtensionPipeline, self).__init__(
            connection_pool,
            response_callbacks,
            transaction,
            shard_hint
        )

        self.make_key = make_key_func

    def pipeline_execute_command(self, *args, **options):
        args = list(args)
        key = args[1]
        args[1] = str(self.make_key(key))
        # print("pipeline exec", args)
        # print("pipeline exec opt", options)

        return super(
            ExtensionPipeline, self
        ).pipeline_execute_command(*args, **options)


class ExtensionClient(DefaultClient):

    def pipeline(self, transaction=True, shard_hint=None):
        client = self.get_client()

        return ExtensionPipeline(
            client.connection_pool,
            client.response_callbacks,
            transaction,
            shard_hint,
            self.make_key)

    def __getattr__(self, cmd):
        client = self.get_client()
        return getattr(client, cmd)


class ExtensionRedisBackend(ExtensionCache, RedisCache):

    def __init__(self, server, params):
        options = params.get("OPTIONS", {})
        cname = "cache_extension.backends.redis.ExtensionClient"
        client_class = options.get('CLIENT_CLASS', cname)
        options['CLIENT_CLASS'] = client_class
        params['options'] = options
        super(ExtensionRedisBackend, self).__init__(server, params)

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

    def pipeline(self, transaction=True, shard_hint=None):
        return self.client.pipeline(transaction=transaction,
                                    shard_hint=shard_hint)

    def __getattr__(self, cmd):
        if cmd not in SUPPORT_CMDS:
            raise KeyError("not supported redis commands")

        func = getattr(self.client, cmd)

        def redis_cmd(key, *args, **kwargs):
            key = self.make_key(key)
            if cmd == 'rename':
                dest = args[0]
                dest = self.make_key(dest)
                args = list(args)
                args[0] = dest

            # print("exec", cmd, key, args, kwargs)
            return func(key, *args, **kwargs)

        return redis_cmd
