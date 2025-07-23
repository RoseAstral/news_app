from django.contrib import admin
from .models import UserProfile, Publisher, Article

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Publisher)
admin.site.register(Article)

class ProfileInline(admin.StackedInline):
    model = UserProfile
