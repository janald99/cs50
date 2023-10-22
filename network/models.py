from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the post
    content = models.TextField()  # The content of the post
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of when the post was created
    likes = models.ManyToManyField(User, related_name='liked_posts')  # Users who liked the post

    def __str__(self):
        return f"Post by {self.user.username} on {self.timestamp}"