# Generated by Django 2.2.6 on 2019-12-06 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statuspost',
            name='likes',
        ),
        migrations.AddField(
            model_name='statuspost',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]