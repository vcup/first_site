from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=50, verbose_name='Song name')
    sid = models.IntegerField(max_length=16, verbose_name='Song id')

    def __str__(self):
        return self.name


class Album(models.Model):
    song = models.ManyToManyField('Song', verbose_name='Album songs')
    name = models.CharField(max_length=50, verbose_name='Album name')
    aid = models.IntegerField(max_length=16, verbose_name='Album id')


class Artist(models.Model):
    song = models.ManyToManyField('Song', verbose_name='Artist songs')
    album = models.ManyToManyField('Album', verbose_name='Artist albums')
    name = models.CharField(max_length=30, verbose_name='Artist name')
    aid = models.IntegerField(max_length=16, verbose_name='Artist id')


class PlayList(models.Model):
    song = models.ManyToManyField('Song', verbose_name='Playlist songs')
    name = models.CharField(max_length=40, verbose_name='Playlist name')
    pid = models.IntegerField(max_length=16, verbose_name='Playlist id')
    type = models.IntegerField(max_length=1, verbose_name='Playlist type')


class User(models.Model):
    song = models.ManyToManyField('Song', verbose_name='User songs')
    playlist = models.ManyToManyField('PlayList', verbose_name='User playlists')
    name = models.CharField(max_length=30, verbose_name='User name')
    uid = models.IntegerField(max_length=16, verbose_name='User id')
