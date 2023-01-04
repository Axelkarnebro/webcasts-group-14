from django.contrib import admin
from .models import Article, Category, Comment, Upcoming_Event
# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Upcoming_Event)