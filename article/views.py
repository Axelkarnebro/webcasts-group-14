from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from .models import Article, Comment
from article.forms import ArticleForm, CommentForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError

class ArticleAuthorMixin(PermissionRequiredMixin):
    def test_func(self):
        if isinstance(self.get_object(), Article):
            return self.request.user in self.get_object().authors.all()

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'title': 'List of Articles',
        'articles': articles
    }

    return render(request, 'pages/article_list.html', context)

class CreateArticle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'pages/article_create.html'
    fields = ['title', 'text']
    permission_required = ('article.add_article',)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        try:
            response = super(CreateArticle, self).form_valid(form)
            form.instance.authors.add(self.request.user)
            
        except IntegrityError as e:
            if 'UNIQUE' in str(e):
                form.add_error('title', "The title for an article must be unique!")
                return self.form_invalid(form)
            raise e
        return response

    def get_success_url(self):
        return reverse('article:article_list')


class UpdateArticle(LoginRequiredMixin, ArticleAuthorMixin, UpdateView):
    model = Article
    template_name = 'pages/article_update.html'
    fields = ['title', 'text']
    permission_required = ('article.change_article',)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        try:
            response = super(UpdateArticle, self).form_valid(form)
        except IntegrityError as e:
            if 'UNIQUE' in str(e):
                form.add_error('title', "The title for an article must be unique!")
                return self.form_invalid(form)
            raise e
        return response

    def get_success_url(self):
        return reverse('article:article_list')



def article_create(request):
    if request.user.is_authenticated:
        if request.user.has_perm('article.add_article'):
            if request.method == 'POST':
                form = ArticleForm(request.POST)

                if form.is_valid():
                    
                    user = request.user.id
                    title = form.cleaned_data['title']
                    text = form.cleaned_data['text']
                    slug = slugify(title)

                    article = Article.objects.create()
                    article.authors.set([user])
                    article.article_title = title
                    article.article_text = text
                    article.slug = slug
                    article.save()
                    
                    return HttpResponseRedirect(reverse('main:thank_you_contact_us'))
                else:
                    
                    print(form.errors)
            else:
                form = ArticleForm()
            return render(request, 'pages/article_create.html', {'form': form})
        
        # If user lacks article creating permissions
        else:
            return HttpResponseRedirect(reverse('main:login_user'))

    else:
        print("fuck u")
        return HttpResponseRedirect(reverse('main:thank_you_contact_us'))

def article_detail(request, slug):
    article = Article.objects.get(slug__exact=slug)
    comments = Comment.objects.filter(article=article)

    context = {
        'article': article,
        'comments': comments
    }

    # Handling comments
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                
                user = request.user
                comment_text = form.cleaned_data['comment_text']

                comment = Comment.objects.create(user=user, article=article, comment_text=comment_text)
                
                return render(request, 'pages/article_detail.html', context)
            else:
                print(form.errors)

    return render(request, 'pages/article_detail.html', context)
