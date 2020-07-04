import decimal
from typing import List

from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=50, verbose_name='单曲名')
    id = models.IntegerField(verbose_name='单曲id', primary_key=True)
    in_album_no = models.IntegerField(default=0, verbose_name='专辑序号')
    pop = models.IntegerField(default=0, verbose_name='人气')
    mvid = models.IntegerField(default=0, verbose_name='MV的id')
    duration = models.IntegerField(default=0, verbose_name='持续时间')

    def duration_str(self):
        t = self.duration / 1000
        last_time = decimal.Decimal(t % 60).quantize(decimal.Decimal('0.000'), rounding=decimal.ROUND_HALF_UP)
        return f'{int(t // 60)}:{last_time}'

    def __str__(self):
        return self.name


class Album(models.Model):
    song = models.ManyToManyField('Song', verbose_name='专辑包涵的单曲')
    name = models.CharField(max_length=50, verbose_name='专辑名')
    id = models.IntegerField(verbose_name='专辑id', primary_key=True)
    pub_date = models.DateTimeField(verbose_name='发布时间')
    company = models.CharField(default='', max_length=50, verbose_name='发行商')
    desc = models.CharField(default='', max_length=1000)
    imgUrl = models.CharField(default='', max_length=100)
    tag = models.ManyToManyField('netease_api.models.Tag', verbose_name='专辑标签')
    type = models.CharField(default='专辑', max_length=50, verbose_name='类型')
    subtype = models.CharField(default='录音室版', max_length=50, verbose_name='子类型')

    def __str__(self):
        return self.name


class Artist(models.Model):
    album = models.ManyToManyField('Album', verbose_name='歌手拥有的专辑')
    name = models.CharField(max_length=30, verbose_name='歌手名')
    id = models.IntegerField(verbose_name='歌手id', primary_key=True)
    user_id = models.IntegerField(default=0, verbose_name='对应用户的id')
    alias = models.ManyToManyField('netease_api.models.Alias', verbose_name='歌手的其他名称')
    desc = models.CharField(default='', max_length=1000, verbose_name='描述')
    imgUrl = models.CharField(default='', max_length=100, verbose_name='头像地址')

    def __str__(self):
        return self.name

    def return_song_set(self) -> list:
        tmp_dict = {}
        [tmp_dict.setdefault(s, None) for a in self.album.all() for s in a.song.all()]
        return list(tmp_dict.keys())


class PlayList(models.Model):
    id = models.IntegerField(verbose_name='歌单ID', primary_key=True)
    master_uid = models.IntegerField(verbose_name='创建该歌单的用户的id')
    name = models.CharField(max_length=40, verbose_name='歌单名称')
    type = models.IntegerField(verbose_name='歌单类型', default=0)
    description = models.CharField(default='', max_length=1000, verbose_name='简介')
    tag = models.CharField(max_length=50, default='[]', verbose_name='歌单标签的json')
    createTime = models.DateTimeField(verbose_name='创建时间')
    imgUrl = models.CharField(max_length=100, verbose_name='封面Url')
    song = models.ManyToManyField('Song', verbose_name='包涵歌曲')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super(PlayList, self).save(**kwargs)
        if not self.user_set.filter(pk=self.master_uid):
            new_master_user = User.objects.get(id=self.master_uid)
            new_master_user.playlist.add(self)
            new_master_user.save()

    def master_user(self) -> 'User':
        return User.objects.get(pk=self.master_uid)


class User(models.Model):
    playlist = models.ManyToManyField('PlayList', verbose_name='用户拥有的歌单')
    name = models.CharField(max_length=30, verbose_name='用户昵称')
    id = models.IntegerField(verbose_name='用户id', primary_key=True)
    createTime = models.DateTimeField(verbose_name='注册时间')
    birthday = models.DateTimeField(verbose_name='生日')
    level = models.IntegerField(default=0, verbose_name='用户等级')
    gender = models.IntegerField(default=0, verbose_name='性别')
    city = models.IntegerField(default=100, verbose_name='所在地')
    avatar_url = models.CharField(default='', max_length=100, verbose_name='头像地址')
    background_url = models.CharField(default='', max_length=100, verbose_name='背景图片地址')
    description = models.CharField(default='', max_length=300, verbose_name='个人介绍')

    def __str__(self):
        return self.name

    def return_song_set(self) -> list:
        tmp_dict = {}
        [tmp_dict.setdefault(s, None) for p in self.playlist.all() for s in p.song.all()]
        return list(tmp_dict.keys())


class Alias(models.Model):
    name = models.CharField(max_length=30, verbose_name='别名')


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name='标签')
