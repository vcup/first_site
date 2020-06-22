from django.test import TestCase

from .models import Song, Album, Artist, PlayList, User  # 有关联的模型


def create_song_data():
    s1 = Song(name='s1', sid=10)
    s1.save()
    s2 = Song(name='s2', sid=20)
    s2.save()
    s3 = Song(name='s3', sid=30)
    s3.save()
    return s1, s2, s3


def create_album_data():
    s1, s2, s3 = create_song_data()
    al1 = Album(name='al1', aid=11)
    al2 = Album(name='al2', aid=21)
    al3 = Album(name='al3', aid=31)
    al1.save(), al2.save(), al3.save()

    al1.song.add(s1)
    al2.song.add(s2, s3)
    al3.song.add(s1, s2, s3)
    al1.save(), al2.save(), al3.save()

    return al1, al2, al3


def create_artist_data():
    al1, al2, al3 = create_album_data()
    a1 = Artist(name='a1', aid=12)
    a2 = Artist(name='a2', aid=22)
    a3 = Artist(name='a3', aid=32)
    a1.save(), a2.save(), a3.save()

    a1.album.add(al1)
    a1.song.add(al1.song.all())

    a2.album.add(al2, al3)
    a2.song.add([s for a in a2.album.all() for s in a.song.all()])

    a3.album.add(al1, al2, al3)
    a3.song.add([s for a in a3.album.all() for s in a.song.all()])

    a1.save(), a2.save(), a3.save()
    return a1, a2, a3


def create_playlist_data():
    s1, s2, s3 = create_song_data()
    p1 = PlayList(name='p1', pid=13)
    p2 = PlayList(name='p2', pid=23)
    p3 = PlayList(name='p3', pid=33)
    p1.save(), p2.save(), p3.save()

    p1.song.add(s1)
    p2.song.add(s2, s3)
    p3.song.add(s1, s2, s3)
    p1.save(), p2.save(), p3.save()

    return p1, p2, p3


def create_user_data():
    p1, p2, p3 = create_playlist_data()
    u1 = User(name='u1', uid=14)
    u2 = User(name='u2', uid=24)
    u3 = User(name='u3', uid=34)
    u1.save(), u2.save(), u3.save()

    u1.playlist.add(p1)
    u2.playlist.add(p2, p3)
    u3.playlist.add(p1, p2, p3)
    u1.save(), u2.save(), u3.save()

    u1.song.add(p1.song.all())
    u2.song.add([s for p in u2.playlist.all() for s in p.song.all()])
    u3.song.add([s for p in u3.playlist.all() for s in p.song.all()])
    u1.save(), u2.save(), u3.save()

    return u1, u2, u3
