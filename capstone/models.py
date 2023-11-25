from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username

class Show(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the show
    title = models.TextField()  # The title of the show
    genre = models.TextField() # The genre the show belongs to
    description = models.TextField() # The description of the show
    rating = models.DecimalField(decimal_places=1, max_digits=3) # Overall rating counted by average
    favorites = models.ManyToManyField(User, related_name='liked_shows')  # Users who favorited the show

    def __str__(self):
        return f"{self.title}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the Review
    show = models.ForeignKey(Show, on_delete=models.CASCADE)  # The show the Review belongs to
    text = models.TextField()  # The Review text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the Review was created

    def __str__(self):
        return f"Review by {self.user.username} on {self.show.title}"
