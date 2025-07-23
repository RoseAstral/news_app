from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, default='READER',)
    follows_user = models.ManyToManyField("self",
                                          related_name="followed_by",
                                          symmetrical=False, blank=True)
    follows_publisher = models.ManyToManyField("Publisher",
                                               related_name="followed_publisher",
                                               symmetrical=False, blank=True)
    working_for_publisher = models.ManyToManyField("Publisher",
                                                   related_name="working_for_publisher",
                                                   symmetrical=False, blank=True)
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
        user_profile.follows_user.set([instance.userprofile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)


class Publisher(models.Model):
    name = models.CharField( max_length=255)
    def __str__(self):
        return self.name


class Article(models.Model):
    journalist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return self.title
