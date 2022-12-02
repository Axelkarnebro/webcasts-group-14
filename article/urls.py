from django.urls import path

from .views import index, article_detail, article_create

app_name = 'article'

urlpatterns = [
    path('', index, name='article_list'),
    
    path('create/', article_create, name='article_create'),
    path('article/<slug:slug>', article_detail, name='article_detail'),
]
