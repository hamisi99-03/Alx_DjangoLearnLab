from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Users this user follows
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username

    def follow(self, other_user):
        if other_user != self:
            self.following.add(other_user)

    def unfollow(self, other_user):
        self.following.remove(other_user)

    def is_following(self, other_user):
        return self.following.filter(pk=other_user.pk).exists()