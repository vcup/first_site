from typing import Tuple

from django.test import TestCase

from .models import Song, Album, Artist, PlayList, User  # 有关联的模型


def create_song_data() -> Tuple[Song, Song, Song]:
    """创建 s1 s2 s3 ，保存并返回"""

    s1 = Song(name='s1', sid=10)
    s1.save()
    s2 = Song(name='s2', sid=20)
    s2.save()
    s3 = Song(name='s3', sid=30)
    s3.save()
    return s1, s2, s3


def create_album_data(s1: Song, s2: Song, s3: Song) -> Tuple[Album, Album, Album]:
    """接受的三个参数 s1、s2、s3 等同于 create_song_data 的返回值
    创建三个 Album，并与 s1、s2、s3 设置关联然后返回，具体的关系为:
        al1: s1
        al2: s1, s2
        al3: s1, s2, s3"""

    al1 = Album(name='al1', aid=11)
    al2 = Album(name='al2', aid=21)
    al3 = Album(name='al3', aid=31)
    al1.save(), al2.save(), al3.save()

    al1.song.add(s1)
    al2.song.add(s1, s2)
    al3.song.add(s1, s2, s3)
    al1.save(), al2.save(), al3.save()

    return al1, al2, al3


def create_artist_data(al1: Album, al2: Album, al3: Album) -> Tuple[Artist, Artist, Artist]:
    """接受的三个参数 al1、al2、al3 等同 create_album_data 的返回值
    创建三个 Artist，并与 al1、al2、al3 及其包涵的 Song 关联然后返回，具体关系为：
        a1: al1(s1); (s1)
        a2: al1(s1), al2(s1, s2); (s1, s2)
        a3: al1(s1), al2(s1, s2), al3(s1, s2, s3); (s1, s2, s3)"""

    a1 = Artist(name='a1', aid=12)
    a2 = Artist(name='a2', aid=22)
    a3 = Artist(name='a3', aid=32)
    a1.save(), a2.save(), a3.save()

    a1.album.add(al1)
    a2.album.add(al1, al2)
    a3.album.add(al1, al2, al3)

    a1.song.add(*al1.song.all())
    a2.song.add(*[s for a in a2.album.all() for s in a.song.all()])
    a3.song.add(*[s for a in a3.album.all() for s in a.song.all()])
    a1.save(), a2.save(), a3.save()
    return a1, a2, a3


def create_playlist_data(s1: Song, s2: Song, s3: Song) -> Tuple[PlayList, PlayList, PlayList]:
    """接受的三个参数 s1、s2、s3 等同于 create_song_data 的返回值
    创建三个 PlayList，并与 s1、s2、s3 关联然后返回，具体关系为：
        p1: s1
        p2: s1, s2
        p3: s1, s2, s3"""

    p1 = PlayList(name='p1', pid=13)
    p2 = PlayList(name='p2', pid=23)
    p3 = PlayList(name='p3', pid=33)
    p1.save(), p2.save(), p3.save()

    p1.song.add(s1)
    p2.song.add(s1, s2)
    p3.song.add(s1, s2, s3)
    p1.save(), p2.save(), p3.save()

    return p1, p2, p3


def create_user_data(p1: PlayList, p2: PlayList, p3: PlayList) -> Tuple[User, User, User]:
    """接受的三个参数 p1, p2, p3 等同 create_playlist_data 的返回值
    创建三个 User，并与 p1、p2、p3 及其包涵的 Song 关联然后返回，具体关系为：
        u1: p1(s1); (s1)
        u2: p1(s1), p2(s1, s2); (s1, s2)
        u3: p1(s1), p2(s1, s2), p3(s1, s2, s3); (s1, s2, s3)"""

    u1 = User(name='u1', uid=14)
    u2 = User(name='u2', uid=24)
    u3 = User(name='u3', uid=34)
    u1.save(), u2.save(), u3.save()

    u1.playlist.add(p1)
    u2.playlist.add(p1, p2)
    u3.playlist.add(p1, p2, p3)
    u1.save(), u2.save(), u3.save()

    u1.song.add(*p1.song.all())
    u2.song.add(*[s for p in u2.playlist.all() for s in p.song.all()])
    u3.song.add(*[s for p in u3.playlist.all() for s in p.song.all()])
    u1.save(), u2.save(), u3.save()

    return u1, u2, u3


class SongModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """为该测试类添加 3*5 个属性"""
        cls.s1, cls.s2, cls.s3 = create_song_data()
        cls.al1, cls.al2, cls.al3 = create_album_data(cls.s1, cls.s2, cls.s3)
        cls.a1, cls.a2, cls.a3 = create_artist_data(cls.al1, cls.al2, cls.al3)
        cls.p1, cls.p2, cls.p3 = create_playlist_data(cls.s1, cls.s2, cls.s3)
        cls.u1, cls.u2, cls.u3 = create_user_data(cls.p1, cls.p2, cls.p3)

    def test_song_name_and_id(self):
        """测试添加 name、sid 时是否正常"""
        s = Song(name='a Song', sid=751472)
        s.save()
        self.assertIs(s.name, 'a Song')
        self.assertIs(s.sid, 751472)

    def test_song_in_album(self):
        """反向查询拥有 Song 的 Album 具体的关系应该是
            s1 in al1, al2, al3
            s2 in al2, al3
            s3 in al3"""

        self.assertEqual(list(self.s3.album_set.all()), [self.al3])
        self.assertEqual(list(self.s2.album_set.all()), [self.al2, self.al3])
        self.assertEqual(list(self.s1.album_set.all()), [self.al1, self.al2, self.al3])

    def test_song_in_artist(self):
        """反向查询拥有 Song 的 Artist 具体的关系应该是
            s1 in a1, a2, a3
            s2 in a2, a3
            a3 in a3"""

        self.assertEqual(list(self.s3.artist_set.all()), [self.a3])
        self.assertEqual(list(self.s2.artist_set.all()), [self.a2, self.a3])
        self.assertEqual(list(self.s1.artist_set.all()), [self.a1, self.a2, self.a3])

    def test_song_in_playlist(self):
        """反向查询拥有 Song 的 PlayList 具体的关系应该是
            s1 in p1, p2, p3
            s2 in p2, p3
            s3 in p3"""

        self.assertEqual(list(self.s3.playlist_set.all()), [self.p3])
        self.assertEqual(list(self.s2.playlist_set.all()), [self.p2, self.p3])
        self.assertEqual(list(self.s1.playlist_set.all()), [self.p1, self.p2, self.p3])

    def test_song_in_user(self):
        """反向查询拥有 Song 的 User 具体关系应该是
            s1 in u1, u2, u3
            s2 in u2, u3
            s3 in u3"""

        self.assertEqual(list(self.s3.user_set.all()), [self.u3])
        self.assertEqual(list(self.s2.user_set.all()), [self.u2, self.u3])
        self.assertEqual(list(self.s1.user_set.all()), [self.u1, self.u2, self.u3])
