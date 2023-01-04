from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='articles')
    title = models.CharField(max_length=50)
    short_desc = models.TextField(max_length=200, null=True, blank=True)
    text = models.TextField(max_length=3000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=300)

class Upcoming_Event(models.Model):
    event_title = models.CharField(max_length=50)
    event_desc = models.TextField(max_length=300)
    date = models.DateField()