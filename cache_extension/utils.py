from django.core.cache import cache
from django.db.models.signals import post_save, post_delete


def apply_decorator(cls):
    def decorator(cls, func):
        def wrapper(*args, **kwargs):
            module_name = cls.__module__
            if module_name.endswith('.cache_keys'):
                module_name = module_name.rsplit('.', 1)[0]

            function_name = func.__name__[len('key_of_'):]

            return '.'.join([module_name, function_name,
                             str(func(*args, **kwargs) or '')])
        return wrapper

    for key, value in cls.__dict__.items():
        if key.startswith('key_of_'):
            setattr(cls, key, staticmethod(decorator(cls, value)))
    return cls


def clear_model_cache(Model, *args, **cache_kwargs):
    def clear_model(sender, instance, **kwargs):
        cache.clear_model(instance)
        if args:
            cache.clear_model(instance, *args)

        fields = cache_kwargs.get('model_list_fields')
        if fields is not None:
            cache.clear_model_list(instance, *fields)

    post_save.connect(clear_model, sender=Model, weak=False)
    post_delete.connect(clear_model, sender=Model, weak=False)
