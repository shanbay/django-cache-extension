from django.db import models
from django.core.cache import cache
from django.utils.functional import curry


class CachedModel(models.Model):

    def _cached_FIELD(self, field):
        value = getattr(self, field.attname)
        Model = field.related_model
        return cache.get_model(Model, pk=value)

    class Meta:
        abstract = True


class ForeignKeyField(models.ForeignKey):
    def contribute_to_class(self, cls, name, **kwargs):
        super(models.ForeignKey, self).contribute_to_class(cls, name, **kwargs)
        if issubclass(cls, models.Model):
            setattr(cls, "cached_%s" % self.name,
                    property(curry(CachedModel._cached_FIELD, field=self)))


class OneToOneField(models.OneToOneField, ForeignKeyField):
    pass
