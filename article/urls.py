from django.urls import path

from .views import index, article_detail, CreateArticle, UpdateArticle, delete_article

app_name = 'article'

urlpatterns = [
    path('', index, name='article_list'),
    
    path('create/', CreateArticle.as_view(), name='article_create'),
    path('article/<slug:slug>', article_detail, name='article_detail'),
    path('article/<slug:slug>/edit', UpdateArticle.as_view(), name='article_update'),
    path('article/<slug:slug>/delete', delete_article, name='delete_article'),
]
