from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

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
