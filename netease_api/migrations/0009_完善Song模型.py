# Generated by Django 3.0.7 on 2020-06-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netease_api', '0008_完善Album模型'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.IntegerField(default=0, verbose_name='持续时间'),
        ),
        migrations.AddField(
            model_name='song',
            name='in_album_no',
            field=models.IntegerField(default=0, verbose_name='专辑序号'),
        ),
        migrations.AddField(
            model_name='song',
            name='mvid',
            field=models.IntegerField(default=0, verbose_name='MV的id'),
        ),
        migrations.AddField(
            model_name='song',
            name='pop',
            field=models.IntegerField(default=0, verbose_name='人气'),
        ),
        migrations.AlterField(
            model_name='song',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='单曲id'),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(max_length=50, verbose_name='单曲名'),
        ),
    ]
