from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the thread
    title = models.TextField()  # The title of the show
    description = models.TextField() # The description of the show
    rating = models.DecimalField(decimal_places=1, max_digits=3) # Overall rating counted by average
    likes = models.ManyToManyField(User, related_name='liked_threads')  # Users who liked the thread

    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the comment
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)  # The thread the comment belongs to
    text = models.TextField()  # The comment text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment was created

    def __str__(self):
        return f"Comment by {self.user.username} on {self.thread.title}"
