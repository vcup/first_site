from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=50, verbose_name='Song name')
    sid = models.IntegerField(verbose_name='Song id')

    def __str__(self):
        return self.name


class Album(models.Model):
    song = models.ManyToManyField('Song', verbose_name='Album songs')
    name = models.CharField(max_length=50, verbose_name='Album name')
    aid = models.IntegerField(verbose_name='Album id')

    def __str__(self):
        return self.name


class Artist(models.Model):
    song = models.ManyToManyField('Song', verbose_name='Artist songs')
    album = models.ManyToManyField('Album', verbose_name='Artist albums')
    name = models.CharField(max_length=30, verbose_name='Artist name')
    aid = models.IntegerField(verbose_name='Artist id')

    def __str__(self):
        return self.name


class PlayList(models.Model):
    song = models.ManyToManyField('Song', verbose_name='包涵歌曲')
    name = models.CharField(max_length=40, verbose_name='歌单名称')
    pid = models.IntegerField(verbose_name='歌单ID')
    type = models.IntegerField(verbose_name='歌单类型', default=0)
    description = models.CharField(max_length=1000, verbose_name='简介')
    ordered = models.BooleanField(default=False, verbose_name='收藏的歌单')
    tag = models.CharField(max_length=50, default='[]', verbose_name='歌单标签的json')  # !此处可以自定义一个JSON字段，继承于CharField
    createTime = models.DateTimeField(verbose_name='创建时间')
    master_user = models.ForeignKey('User',
                                    on_delete=models.CASCADE,
                                    related_name='Playlist_Master',
                                    verbose_name='创建该歌单的用户'
                                    )

    def __str__(self):
        return self.name


class User(models.Model):
    song = models.ManyToManyField('Song', verbose_name='User songs')
    playlist = models.ManyToManyField('PlayList', verbose_name='User playlists')
    name = models.CharField(max_length=30, verbose_name='User name')
    uid = models.IntegerField(verbose_name='User id')

    def __str__(self):
        return self.name
