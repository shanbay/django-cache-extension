from django.db import models
from django.core.cache import cache
from django.utils.functional import curry


class CachedModel(models.Model):

    def _cached_FIELD(self, field, cache_exc):
        value = getattr(self, field.attname)
        Model = field.related_model
        return cache.get_model(Model, pk=value, cache_exc=cache_exc)

    class Meta:
        abstract = True


class ForeignKeyField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        self.cache_exc = kwargs.pop('cache_exc', False)
        super(ForeignKeyField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super(models.ForeignKey, self).contribute_to_class(cls, name, **kwargs)
        if issubclass(cls, models.Model):
            setattr(cls, "cached_%s" % self.name,
                    property(curry(CachedModel._cached_FIELD, field=self,
                                   cache_exc=self.cache_exc)))


class OneToOneField(models.OneToOneField, ForeignKeyField):
    pass
