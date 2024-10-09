from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  
    # Override the groups field
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Unique related name
        blank=True,
    )

    # Override the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Unique related name
        blank=True,
    )
    def __str__(self):
        return self.username

class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    




