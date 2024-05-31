from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=1)
    image_url = models.ImageField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_set")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_set")
    created_at = models.DateTimeField(auto_now_add=True)
    
class Bid(models.Model):
    amount = models.FloatField(default=0.0)  
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_set")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_set")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
