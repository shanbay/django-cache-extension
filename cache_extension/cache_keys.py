from django.db.models import ForeignKey
try:
    from django.core.exceptions import FieldDoesNotExist
except:
    # for old django version
    from django.db.models.fields import FieldDoesNotExist

def key_of_model(cls, *args, **kwargs):
    key_prefix = "%s.%s" % (cls.__module__, cls.__name__)

    if hasattr(cls, 'cache_version'):
        key_prefix += ".%s" % (getattr(cls, 'cache_version'))

    if args:
        if len(args) != 2:
            raise ValueError('args must be [field, val]')
        keys = "%s.%s" % (args[0], args[1])
    else:
        valid, msg = validate_fields(cls, kwargs)
        if not valid:
            raise ValueError(msg)
        keys = sorted(["%s.%s" % item for item in kwargs.items()])
        keys = '.'.join(keys)
    return "%s.%s" % (key_prefix, keys)


def key_of_model_list(cls, **kwargs):

    valid, msg = validate_fields(cls, kwargs)
    if not valid:
        raise ValueError(msg)

    key_prefix = "list.%s.%s" % (cls.__module__, cls.__name__)
    if hasattr(cls, 'list_cache_version'):
        key_prefix += ".%s" % (getattr(cls, 'list_cache_version'))

    # if len(kwargs) == 0 means i want get all
    if hasattr(cls, 'list_cache_version'):
        key_prefix += ".%s" % (getattr(cls, 'list_cache_version'))
    keys = sorted(["%s.%s" % item for item in kwargs.items()])
    keys = '.'.join(keys)
    return "%s.%s" % (key_prefix, keys)


def validate_fields(cls, fields):
    for key, value in fields.items():
        if key in ['pk', 'id']:
            continue
        if not key.endswith('_id') and '__' not in key:
            field = cls._meta.get_field(key)
            if isinstance(field, ForeignKey):
                return False, 'must use FIELD_id on related fields'
    return True, 'SUCCESS'
