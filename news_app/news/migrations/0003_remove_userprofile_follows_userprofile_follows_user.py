# Generated by Django 5.2.4 on 2025-07-21 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_userprofile_follows"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="follows",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="follows_user",
            field=models.ManyToManyField(
                blank=True, related_name="followed_by", to="news.userprofile"
            ),
        ),
    ]
