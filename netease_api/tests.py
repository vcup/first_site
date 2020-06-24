from django.test import TestCase
from django.utils import timezone

from .models import Song, Album, Artist, PlayList, User  # 有关联的模型


class ModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.s1 = Song.objects.create(name='s1', id=10)
        cls.s2 = Song.objects.create(name='s2', id=20)
        cls.s3 = Song.objects.create(name='s3', id=30)
        cls.s1.save(), cls.s2.save(), cls.s3.save()

        cls.al1 = Album.objects.create(name='al1', id=11)
        cls.al2 = Album.objects.create(name='al2', id=21)
        cls.al3 = Album.objects.create(name='al3', id=31)
        cls.al1.save(), cls.al2.save(), cls.al3.save()

        cls.a1 = Artist.objects.create(name='a1', id=12)
        cls.a2 = Artist.objects.create(name='a2', id=22)
        cls.a3 = Artist.objects.create(name='a3', id=32)

        cls.u1 = User.objects.create(name='u1', id=14)
        cls.u2 = User.objects.create(name='u2', id=24)
        cls.u3 = User.objects.create(name='u3', id=34)

        cls.p1 = PlayList.objects.create(name='p1', id=13, createTime=timezone.now(), master_uid=34)
        cls.p2 = PlayList.objects.create(name='p2', id=23, type=5, createTime=timezone.now(), master_uid=34)
        cls.p3 = PlayList.objects.create(name='p3', id=33, type=1, createTime=timezone.now(), master_uid=34)

        cls.a1.album.add(cls.al1)
        cls.a2.album.add(cls.al1, cls.al2)
        cls.a3.album.add(cls.al1, cls.al2, cls.al3)
        cls.a1.save(), cls.a2.save(), cls.a3.save()

        cls.al1.song.add(cls.s1)
        cls.al2.song.add(cls.s1, cls.s2)
        cls.al3.song.add(cls.s1, cls.s2, cls.s3)
        cls.al1.save(), cls.al2.save(), cls.al3.save()

        cls.p1.song.add(cls.s1)
        cls.p2.song.add(cls.s1, cls.s2)
        cls.p3.song.add(cls.s1, cls.s2, cls.s3)
        cls.al1.save(), cls.al2.save(), cls.al3.save()

        cls.u1.playlist.add(cls.p1)
        cls.u2.playlist.add(cls.p1, cls.p2)
        cls.u1.save(), cls.u2.save()


class SongModelTests(ModelTests):

    def test_song_name(self):
        self.assertEqual((self.s1.name, self.s2.name, self.s3.name), ('s1', 's2', 's3'))

    def test_song_id(self):
        self.assertEqual((self.s1.id, self.s2.id, self.s3.id), (10, 20, 30))

    def test_s1_in_album(self):
        self.assertEqual(list(self.s3.album_set.all()), [self.al3])

    def test_s2_in_album(self):
        self.assertEqual(list(self.s2.album_set.all()), [self.al2, self.al3])

    def test_s3_in_album(self):
        self.assertEqual(list(self.s1.album_set.all()), [self.al1, self.al2, self.al3])

    def test_s1_in_playlist(self):
        self.assertEqual(list(self.s3.playlist_set.all()), [self.p3])

    def test_s2_in_playlist(self):
        self.assertEqual(list(self.s2.playlist_set.all()), [self.p2, self.p3])

    def test_s3_in_playlist(self):
        self.assertEqual(list(self.s1.playlist_set.all()), [self.p1, self.p2, self.p3])


class AlbumModelTests(ModelTests):
    """与模型 Song 相关的东西在 SongModelTests 中已经测试的差不多了，所以本测试类只专注于 Song 以外的点"""

    def test_album_name(self):
        self.assertEqual((self.al1.name, self.al2.name, self.al3.name), ('al1', 'al2', 'al3'))

    def test_album_id(self):
        self.assertEqual((self.al1.id, self.al2.id, self.al3.id), (11, 21, 31))

    def test_al1_in_artist(self):
        self.assertEqual(list(self.al3.artist_set.all()), [self.a3])

    def test_al2_in_artist(self):
        self.assertEqual(list(self.al2.artist_set.all()), [self.a2, self.a3])

    def test_al3_in_artist(self):
        self.assertEqual(list(self.al1.artist_set.all()), [self.a1, self.a2, self.a3])


class ArtistModelTests(ModelTests):

    def test_artist_name(self):
        self.assertEqual((self.a1.name, self.a2.name, self.a3.name), ('a1', 'a2', 'a3'))

    def test_artist_id(self):
        self.assertEqual((self.a1.id, self.a2.id, self.a3.id), (12, 22, 32))

    def test_a1_have_song(self):
        self.assertEqual(self.a1.return_self_have_song(), [[self.s1]])

    def test_a2_have_song(self):
        self.assertEqual(self.a2.return_self_have_song(), [[self.s1], [self.s1, self.s2]])

    def test_a3_have_song(self):
        self.assertEqual(self.a3.return_self_have_song(), [[self.s1], [self.s1, self.s2], [self.s1, self.s2, self.s3]])


class PlayListModelTests(ModelTests):

    def test_playlist_name(self):
        self.assertEqual((self.p1.name, self.p2.name, self.p3.name), ('p1', 'p2', 'p3'))

    def test_playlist_id(self):
        self.assertEqual((self.p1.id, self.p2.id, self.p3.id), (13, 23, 33))

    def test_playlist_type(self):
        self.assertEqual((self.p1.type, self.p2.type, self.p3.type), (0, 5, 1))

    def test_p1_have_song(self):
        self.assertEqual(list(self.p1.song.all()), [self.s1])

    def test_p2_have_song(self):
        self.assertEqual(list(self.p2.song.all()), [self.s1, self.s2])

    def test_p3_have_song(self):
        self.assertEqual(list(self.p3.song.all()), [self.s1, self.s2, self.s3])


class UserModelTests(ModelTests):

    def test_user_name(self):
        self.assertEqual((self.u1.name, self.u2.name, self.u3.name), ('u1', 'u2', 'u3'))

    def test_user_id(self):
        self.assertEqual((self.u1.id, self.u2.id, self.u3.id), (14, 24, 34))

    def test_u1_have_playlist(self):
        self.assertEqual(list(self.u1.playlist.all()), [self.p1])

    def test_u2_have_playlist(self):
        self.assertEqual(list(self.u2.playlist.all()), [self.p1, self.p2])

    def test_u3_have_playlist(self):
        self.assertEqual(list(self.u3.playlist.all()), [self.p1, self.p2, self.p3])

    def test_u3_have_self_created_playlist(self):
        self.assertEqual(list(self.u1.playlist.all()), [self.p1, self.p3])
