# Generated by Django 3.0.7 on 2020-06-24 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netease_api', '0004_将master_user改成master_id_并且为相关模型添加了查询方法'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='ordered',
        ),
    ]
