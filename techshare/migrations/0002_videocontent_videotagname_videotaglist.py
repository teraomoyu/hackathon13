# Generated by Django 4.0.1 on 2022-01-23 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techshare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('upload_date', models.DateTimeField()),
                ('original_name', models.CharField(max_length=200)),
                ('filename', models.CharField(default='', max_length=200)),
                ('thumb_frame', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VideoTagName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VideoTagList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techshare.videocontent')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techshare.videotagname')),
            ],
        ),
    ]
