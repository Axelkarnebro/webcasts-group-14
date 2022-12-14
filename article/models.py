from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='articles')
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=3000)
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=300)

class Upcoming_Event(models.Model):
    event_title = models.CharField(max_length=50)
    event_desc = models.TextField(max_length=300)
    date = models.DateField()