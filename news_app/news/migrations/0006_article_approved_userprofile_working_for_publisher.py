# Generated by Django 5.2.4 on 2025-07-22 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0005_alter_userprofile_follows_publisher"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="approved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="working_for_publisher",
            field=models.ManyToManyField(
                blank=True, related_name="working_for_publisher", to="news.publisher"
            ),
        ),
    ]
