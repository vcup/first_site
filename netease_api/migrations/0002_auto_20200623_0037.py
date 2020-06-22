# Generated by Django 3.0.7 on 2020-06-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netease_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='aid',
            field=models.IntegerField(verbose_name='Album id'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='aid',
            field=models.IntegerField(verbose_name='Artist id'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='pid',
            field=models.IntegerField(verbose_name='Playlist id'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='type',
            field=models.IntegerField(verbose_name='Playlist type'),
        ),
        migrations.AlterField(
            model_name='song',
            name='sid',
            field=models.IntegerField(verbose_name='Song id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.IntegerField(verbose_name='User id'),
        ),
    ]
