from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=250)
    short_desc = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    desc = models.TextField(blank=True,null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'