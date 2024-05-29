from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)
    info_link = models.URLField(blank=True)
    image = models.URLField(blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  
    like = models.BooleanField(default=False)  
    comment = models.TextField(blank=True) 

    def __str__(self):
        return f"{self.user.username} interacted with {self.book.title}"
