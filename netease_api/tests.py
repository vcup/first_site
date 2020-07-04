from django.test import TestCase
from django.utils import timezone

from .models import Song, Album, Artist, PlayList, User  # 有关联的模型


class ModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        cls.s1 = Song.objects.create(name='s1', id=10, duration=89051)
        cls.s2 = Song.objects.create(name='s2', id=20, duration=215400)
        cls.s3 = Song.objects.create(name='s3', id=30, duration=260996)

        cls.al1 = Album.objects.create(name='al1', id=11, pub_date=now)
        cls.al2 = Album.objects.create(name='al2', id=21, pub_date=now)
        cls.al3 = Album.objects.create(name='al3', id=31, pub_date=now)

        cls.a1 = Artist.objects.create(name='a1', id=12)
        cls.a2 = Artist.objects.create(name='a2', id=22)
        cls.a3 = Artist.objects.create(name='a3', id=32)

        cls.u1 = User.objects.create(name='u1', id=14, createTime=now, birthday=now)
        cls.u2 = User.objects.create(name='u2', id=24, createTime=now, birthday=now)
        cls.u3 = User.objects.create(name='u3', id=34, createTime=now, birthday=now)

        cls.p1 = PlayList.objects.create(name='p1', id=13, createTime=now, master_uid=34)
        cls.p2 = PlayList.objects.create(name='p2', id=23, type=5, createTime=now, master_uid=34)
        cls.p3 = PlayList.objects.create(name='p3', id=33, type=1, createTime=now, master_uid=34)

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
        self.assertEqual(('s1', 's2', 's3'), (self.s1.name, self.s2.name, self.s3.name))

    def test_song_id(self):
        self.assertEqual((10, 20, 30), (self.s1.id, self.s2.id, self.s3.id))

    def test_s1_in_album(self):
        self.assertEqual([self.al3], list(self.s3.album_set.all()))

    def test_s2_in_album(self):
        self.assertEqual([self.al2, self.al3], list(self.s2.album_set.all()))

    def test_s3_in_album(self):
        self.assertEqual([self.al1, self.al2, self.al3], list(self.s1.album_set.all()))

    def test_s1_in_playlist(self):
        self.assertEqual([self.p1, self.p2, self.p3], list(self.s1.playlist_set.all()))

    def test_s2_in_playlist(self):
        self.assertEqual([self.p2, self.p3], list(self.s2.playlist_set.all()))

    def test_s3_in_playlist(self):
        self.assertEqual([self.p3], list(self.s3.playlist_set.all()))

    def test_s1_duration_str(self):
        self.assertEqual('1:29.051', self.s1.duration_str())

    def test_s2_duration_str(self):
        self.assertEqual('3:35.400', self.s2.duration_str())

    def test_s3_duration_str(self):
        self.assertEqual('4:20.996', self.s3.duration_str())


class AlbumModelTests(ModelTests):

    def test_album_name(self):
        self.assertEqual(('al1', 'al2', 'al3'), (self.al1.name, self.al2.name, self.al3.name))

    def test_album_id(self):
        self.assertEqual((11, 21, 31), (self.al1.id, self.al2.id, self.al3.id))

    def test_al1_in_artist(self):
        self.assertEqual([self.a1, self.a2, self.a3], list(self.al1.artist_set.all()))

    def test_al2_in_artist(self):
        self.assertEqual([self.a2, self.a3], list(self.al2.artist_set.all()))

    def test_al3_in_artist(self):
        self.assertEqual([self.a3], list(self.al3.artist_set.all()))


class ArtistModelTests(ModelTests):

    def test_artist_name(self):
        self.assertEqual(('a1', 'a2', 'a3'), (self.a1.name, self.a2.name, self.a3.name))

    def test_artist_id(self):
        self.assertEqual((12, 22, 32), (self.a1.id, self.a2.id, self.a3.id))

    def test_a1_have_album(self):
        self.assertEqual([self.al1], list(self.a1.album.all()))

    def test_a2_have_album(self):
        self.assertEqual([self.al1, self.al2], list(self.a2.album.all()))

    def test_a3_have_album(self):
        self.assertEqual([self.al1, self.al2, self.al3], list(self.a3.album.all()))

    def test_a1_song_set(self):
        self.assertEqual([self.s1], self.a1.return_song_set())

    def test_a2_song_set(self):
        self.assertEqual([self.s1, self.s2], self.a2.return_song_set())

    def test_a3_song_set(self):
        self.assertEqual([self.s1, self.s2, self.s3], self.a3.return_song_set())


class PlayListModelTests(ModelTests):

    def test_playlist_name(self):
        self.assertEqual(('p1', 'p2', 'p3'), (self.p1.name, self.p2.name, self.p3.name))

    def test_playlist_id(self):
        self.assertEqual((13, 23, 33), (self.p1.id, self.p2.id, self.p3.id))

    def test_playlist_type(self):
        self.assertEqual((0, 5, 1), (self.p1.type, self.p2.type, self.p3.type))

    def test_p1_have_song(self):
        self.assertEqual([self.s1], list(self.p1.song.all()))

    def test_p2_have_song(self):
        self.assertEqual([self.s1, self.s2], list(self.p2.song.all()))

    def test_p3_have_song(self):
        self.assertEqual([self.s1, self.s2, self.s3], list(self.p3.song.all()))

    def test_p1_in_user(self):
        self.assertEqual([self.u3, self.u1, self.u2], list(self.p1.user_set.all()))

    def test_p2_in_user(self):
        self.assertEqual([self.u3, self.u2], list(self.p2.user_set.all()))

    def test_p3_in_user(self):
        self.assertEqual([self.u3], list(self.p3.user_set.all()))


class UserModelTests(ModelTests):

    def test_user_name(self):
        self.assertEqual(('u1', 'u2', 'u3'), (self.u1.name, self.u2.name, self.u3.name))

    def test_user_id(self):
        self.assertEqual((14, 24, 34), (self.u1.id, self.u2.id, self.u3.id))

    def test_u1_have_playlist(self):
        self.assertEqual([self.p1], list(self.u1.playlist.all()))

    def test_u2_have_playlist(self):
        self.assertEqual([self.p1, self.p2], list(self.u2.playlist.all()))

    def test_u3_have_playlist(self):
        self.assertEqual([self.p1, self.p2, self.p3], list(self.u3.playlist.all()))

    def test_u3_have_self_created_playlist(self):
        self.assertEqual([self.p1], list(self.u1.playlist.all()))

    def test_u1_song_set(self):
        self.assertEqual([self.s1], self.u1.return_song_set())

    def test_u2_song_set(self):
        self.assertEqual([self.s1, self.s2], self.u2.return_song_set())

    def test_u3_song_set(self):
        self.assertEqual([self.s1, self.s2, self.s3], self.u3.return_song_set())
