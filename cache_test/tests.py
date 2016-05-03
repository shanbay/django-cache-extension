from django.test import TestCase
from django.core.cache import cache
from redis.exceptions import ResponseError
from cache_extension.utils import apply_decorator
from .models import Album


class CacheTest(TestCase):
    fixtures = ['albums.json']

    def setUp(self):
        all_albums = Album.objects.filter(artist="Taylor Swift")
        self.num_albums = all_albums.count()
        self.album_ids = all_albums.values_list('id', flat=True)

    def tearDown(self):
        Album.objects.all().delete()
        cache.clear()

    def test_cache(self):
        album = cache.get_model(
            Album, artist="Taylor Swift", title="Taylor Swift")
        self.assertEqual(album.artist, "Taylor Swift")
        try:
            album = cache.get_model(Album, artist="Tay-Tay")
        except Album.DoesNotExist:
            album = cache.get_model(
                Album, cache_exist=True, artist="Tay-Tay")
        self.assertEqual(album, None)
        Album(artist="Tay-Tay", title="1989").save()
        result_model = cache.get_model(
            Album, cache_exist=True, artist="Tay-Tay")
        self.assertEqual(result_model.artist, "Tay-Tay")

        albums = cache.get_model_list(Album, artist="Taylor Swift")
        self.assertEqual(len(albums), self.num_albums)

        albums = cache.get_models(Album, self.album_ids)
        self.assertEqual(len(albums), len(self.album_ids))

        album = Album.objects.create(artist="Tay-Tay", title="Red")
        cache.set_model(album)
        all_albums = Album.objects.all()
        result_album = cache.get_model(Album, album.pk)
        self.assertEqual(album.pk, result_album.pk)

        cache.set_model_list(Album, artist="Tay-Tay")
        num_albums = Album.objects.filter(artist="Tay-Tay").count()
        albums_tay = cache.get_model_list(Album, artist="Tay-Tay")
        self.assertEqual(len(albums_tay), num_albums)
        cache.clear_models(Album, 'artist', ["Tay-Tay"])

    def test_incr(self):
        key = "album_total_num"
        cache.set(key, self.num_albums)
        result = cache.incr(key, 1)
        self.assertEqual(result, self.num_albums+1)
        cache.set(key, "album num")
        try:
            result = cache.incr(key, 1)
        except ResponseError:
            pass

    def test_cache_decorator(self):

        @apply_decorator
        class Cache_key:

            def key_of_test_cache_key(id):
                return '%s_v1' % id

        self.assertEqual(Cache_key.key_of_test_cache_key(1),
                         'cache_test.test.test_cache_key.1_v1')
