# Generated by Django 3.0 on 2019-12-11 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Qsystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='papercomment',
            name='comment_topic',
            field=models.CharField(default='请输入标题', max_length=256),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='comment_topic',
            field=models.CharField(default='请输入标题', max_length=256),
        ),
    ]