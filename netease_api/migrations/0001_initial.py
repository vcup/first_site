# Generated by Django 3.0.7 on 2020-06-23 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Album name')),
                ('aid', models.IntegerField(verbose_name='Album id')),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='歌单名称')),
                ('pid', models.IntegerField(verbose_name='歌单ID')),
                ('type', models.IntegerField(default=0, verbose_name='歌单类型')),
                ('description', models.CharField(max_length=1000, verbose_name='简介')),
                ('ordered', models.BooleanField(default=False, verbose_name='收藏的歌单')),
                ('tag', models.CharField(default='[]', max_length=50, verbose_name='歌单标签的json')),
                ('createTime', models.DateTimeField(verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Song name')),
                ('sid', models.IntegerField(verbose_name='Song id')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='User name')),
                ('uid', models.IntegerField(verbose_name='User id')),
                ('playlist', models.ManyToManyField(to='netease_api.PlayList', verbose_name='User playlists')),
                ('song', models.ManyToManyField(to='netease_api.Song', verbose_name='User songs')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='master_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Playlist_Master', to='netease_api.User', verbose_name='创建该歌单的用户'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='song',
            field=models.ManyToManyField(to='netease_api.Song', verbose_name='包涵歌曲'),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Artist name')),
                ('aid', models.IntegerField(verbose_name='Artist id')),
                ('album', models.ManyToManyField(to='netease_api.Album', verbose_name='Artist albums')),
                ('song', models.ManyToManyField(to='netease_api.Song', verbose_name='Artist songs')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='song',
            field=models.ManyToManyField(to='netease_api.Song', verbose_name='Album songs'),
        ),
    ]
