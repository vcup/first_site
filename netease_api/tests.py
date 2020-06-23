from django.test import TestCase
from django.utils import timezone

from .models import Song, Album, Artist, PlayList, User  # 有关联的模型


class ModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.s1 = Song(name='s1', sid=10)
        cls.s2 = Song(name='s2', sid=20)
        cls.s3 = Song(name='s3', sid=30)
        cls.s1.save(), cls.s2.save(), cls.s3.save()

        cls.al1 = Album(name='al1', aid=11)
        cls.al2 = Album(name='al2', aid=21)
        cls.al3 = Album(name='al3', aid=31)
        cls.al1.save(), cls.al2.save(), cls.al3.save()

        cls.a1 = Artist(name='a1', aid=12)
        cls.a2 = Artist(name='a2', aid=22)
        cls.a3 = Artist(name='a3', aid=32)
        cls.a1.save(), cls.a2.save(), cls.a3.save()

        cls.u1 = User(name='u1', uid=14)
        cls.u2 = User(name='u2', uid=24)
        cls.u3 = User(name='u3', uid=34)
        cls.u1.save(), cls.u2.save(), cls.u3.save()

        cls.p1 = PlayList(name='p1', pid=13, createTime=timezone.now(), master_user=cls.u3)
        cls.p2 = PlayList(name='p2', pid=23, type=5, createTime=timezone.now(), master_user=cls.u3)
        cls.p3 = PlayList(name='p3', pid=33, type=1, createTime=timezone.now(), master_user=cls.u3)
        cls.p1.save(), cls.p2.save(), cls.p3.save()

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
        cls.u3.playlist.add(cls.p1, cls.p2, cls.p3)
        cls.u1.save(), cls.u2.save(), cls.u3.save()


class SongModelTests(ModelTests):

    def test_song_name(self):
        self.assertEqual((self.s1.name, self.s2.name, self.s3.name), ('s1', 's2', 's3'))

    def test_song_id(self):
        self.assertEqual((self.s1.sid, self.s2.sid, self.s3.sid), (10, 20, 30))

    def test_song_in_album(self):
        """反向查询拥有 Song 的 Album 具体的关系应该是
            s1 in al1, al2, al3
            s2 in al2, al3
            s3 in al3"""

        self.assertEqual(list(self.s3.album_set.all()), [self.al3])
        self.assertEqual(list(self.s2.album_set.all()), [self.al2, self.al3])
        self.assertEqual(list(self.s1.album_set.all()), [self.al1, self.al2, self.al3])

    def test_song_in_playlist(self):
        """反向查询拥有 Song 的 PlayList 具体的关系应该是
            s1 in p1, p2, p3
            s2 in p2, p3
            s3 in p3"""

        self.assertEqual(list(self.s3.playlist_set.all()), [self.p3])
        self.assertEqual(list(self.s2.playlist_set.all()), [self.p2, self.p3])
        self.assertEqual(list(self.s1.playlist_set.all()), [self.p1, self.p2, self.p3])


class AlbumModelTests(ModelTests):
    """与模型 Song 相关的东西在 SongModelTests 中已经测试的差不多了，所以本测试类只专注于 Song 以外的点"""

    def test_album_name(self):
        self.assertEqual((self.al1.name, self.al2.name, self.al3.name), ('al1', 'al2', 'al3'))

    def test_album_id(self):
        self.assertEqual((self.al1.aid, self.al2.aid, self.al3.aid), (11, 21, 31))

    def test_album_in_artist(self):
        self.assertEqual(list(self.al3.artist_set.all()), [self.a3])
        self.assertEqual(list(self.al2.artist_set.all()), [self.a2, self.a3])
        self.assertEqual(list(self.al1.artist_set.all()), [self.a1, self.a2, self.a3])


class ArtistModelTests(ModelTests):

    def test_artist_name(self):
        self.assertEqual((self.a1.name, self.a2.name, self.a3.name), ('a1', 'a2', 'a3'))

    def test_artist_id(self):
        self.assertEqual((self.a1.aid, self.a2.aid, self.a3.aid), (12, 22, 32))

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
        self.assertEqual((self.p1.pid, self.p2.pid, self.p3.pid), (13, 23, 33))

    def test_playlist_type(self):
        self.assertEqual((self.p1.type, self.p2.type, self.p3.type), (0, 5, 1))


class UserModelTests(ModelTests):

    def test_user_name(self):
        self.assertEqual((self.u1.name, self.u2.name, self.u3.name), ('u1', 'u2', 'u3'))

    def test_user_id(self):
        self.assertEqual((self.u1.uid, self.u2.uid, self.u3.uid), (14, 24, 34))

    def test_u1_have_song(self):
        self.assertEqual(self.u1.return_self_have_song(), [[self.s1]])

    def test_u2_have_song(self):
        self.assertEqual(self.u2.return_self_have_song(), [[self.s1], [self.s1, self.s2]])

    def test_u3_have_song(self):
        self.assertEqual(self.u3.return_self_have_song(), [[self.s1], [self.s1, self.s2], [self.s1, self.s2, self.s3]])
