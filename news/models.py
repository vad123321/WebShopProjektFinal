from django.db import models
from django.contrib.auth.models import User

class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return (self.name)

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (self.title)