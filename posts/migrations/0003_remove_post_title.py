# Generated by Django 4.0.1 on 2022-01-21 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_updated_at_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
