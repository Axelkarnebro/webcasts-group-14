from django.urls import path

from .views import index, article_detail, CreateArticle

app_name = 'article'

urlpatterns = [
    path('', index, name='article_list'),
    
    path('create/', CreateArticle.as_view(), name='article_create'),
    path('article/<slug:slug>', article_detail, name='article_detail'),
]
