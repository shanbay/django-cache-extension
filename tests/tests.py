from django.test import TestCase
from django.core.cache import cache
from django.core.cache import caches
from cache_extension.utils import apply_decorator
from cache_extension import cache_keys
from .models import Album


class CacheTest(TestCase):
    fixtures = ['albums.json']

    def setUp(self):
        all_albums = Album.objects.filter(artist="Taylor Swift")
        self.num_albums = all_albums.count()
        self.album_ids = all_albums.values_list('id', flat=True)
        self.redis_cache = caches['redis']

    def tearDown(self):
        Album.objects.all().delete()
        cache.clear()

    def test_cache(self):
        album = cache.get_model(Album, artist="Taylor Swift",
                                title="Taylor Swift")
        self.assertEqual(album.artist, "Taylor Swift")

        try:
            album = cache.get_model(Album, artist="Tay-Tay")
        except Album.DoesNotExist:
            album = cache.get_model(Album, cache_exc=True, artist="Tay-Tay")

        self.assertEqual(album, None)

        Album(artist="Tay-Tay", title="1989").save()

        result_model = cache.get_model(Album, cache_exc=True, artist="Tay-Tay")
        self.assertEqual(result_model.artist, "Tay-Tay")

        albums = cache.get_model_list(Album, artist="Taylor Swift")
        self.assertEqual(len(albums), self.num_albums)

        albums = cache.get_models(Album, self.album_ids)
        self.assertEqual(len(albums), len(self.album_ids))

        album = Album.objects.create(artist="Tay-Tay", title="Red")
        cache.set_model(album)
        result_album = cache.get_model(Album, pk=album.pk)
        self.assertEqual(album.pk, result_album.pk)

        cache.set_model_list(Album, artist="Tay-Tay")
        num_albums = Album.objects.filter(artist="Tay-Tay").count()
        albums_tay = cache.get_model_list(Album, artist="Tay-Tay")
        self.assertEqual(len(albums_tay), num_albums)
        cache.clear_models(Album, 'artist', ["Tay-Tay"])

    def test_add_model_field(self):
        album = Album.objects.get(pk=1)
        result = {
            f.attname: getattr(album, f.attname) for f in album._meta.fields
        }
        result['another_field'] = '1'

        key = cache_keys.key_of_model(Album, pk=1)
        cache.set(key, result)
        key = cache_keys.key_of_model_list(Album, artist="Taylor Swift")
        cache.set(key, [result])

        album = cache.get_model(Album, pk=1)
        self.assertRaises(AttributeError, lambda: album.another_field)

    def test_incr(self):
        key = "album_total_num"
        cache.set(key, self.num_albums)
        result = cache.incr(key, 1)
        self.assertEqual(result, self.num_albums+1)

    def test_other_cmd(self):
        key = "album_ids"
        ids = self.redis_cache.smembers(key)
        self.assertEqual(ids, set([]))

    def test_cache_decorator(self):

        @apply_decorator
        class Cache_key:

            def key_of_test_cache_key(id):
                return '%s_v1' % id

        self.assertEqual(Cache_key.key_of_test_cache_key(1),
                         'tests.tests.test_cache_key.1_v1')
