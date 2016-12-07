from django.db import models
from cache_extension.utils import clear_model_cache


# Create your models here.
class Album(models.Model):
    artist = models.CharField(max_length=128)
    title = models.CharField(max_length=128)

clear_model_cache(Album)
clear_model_cache(Album, 'artist')
clear_model_cache(Album, model_list_fields=['artist'])
