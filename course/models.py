from django.db import models

from django.conf import settings


class CourseCommonInfo(models.Model):
    short_desc = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=False,
                            null=True)  # hyphenated lower case text of the title

    class Meta:
        abstract = True


# Create your models here.
class Course(CourseCommonInfo):
    COURSE_STATUS = (
        ('PUB', 'Published'),
        ('UNP', 'UnPublished'),
        ('CSN', 'Coming Soon')
    )

    title = models.CharField(max_length=250, unique=True)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses')
    status = models.CharField(max_length=3, choices=COURSE_STATUS, default="UNP")
    subscriptions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscribed_courses',
                                           through='CourseSubscription')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'


class CourseSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_subscribed = models.DateField(null=True)


class CourseClass(CourseCommonInfo):
    title = models.CharField(max_length=250)
    is_free = models.BooleanField(default=False)
    course = models.ForeignKey(Course, related_name='classes', on_delete=models.CASCADE)