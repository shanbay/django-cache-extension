def key_of_model(cls, *args, **kwargs):
    key_prefix = "%s.%s" % (cls.__module__, cls.__name__)

    if hasattr(cls, 'cache_version'):
        key_prefix += ".%s" % (getattr(cls, 'cache_version'))

    if args:
        if len(args) != 2:
            raise ValueError('args must be [field, val]')
        keys = "%s.%s" % (args[0], args[1])
    else:
        keys = sorted(["%s.%s" % item for item in kwargs.items()])
        keys = '.'.join(keys)
    return "%s.%s" % (key_prefix, keys)


def key_of_model_list(cls, **kwargs):
    key_prefix = "%s.%s" % (cls.__module__, cls.__name__)
    if hasattr(cls, 'list_cache_version'):
        key_prefix += ".%s" % (getattr(cls, 'list_cache_version'))

    # if len(kwargs) == 0 means i want get all
    if hasattr(cls, 'list_cache_version'):
        key_prefix += ".%s" % (getattr(cls, 'list_cache_version'))
    keys = sorted(["%s.%s" % item for item in kwargs.items()])
    keys = '.'.join(keys)
    return "%s.%s" % (key_prefix, keys)
