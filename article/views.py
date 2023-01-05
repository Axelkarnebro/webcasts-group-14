from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from .models import Article, Category, Comment
from article.forms import ArticleForm, CommentForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError


from django.views.decorators.cache import cache_page

class ArticleAuthorMixin(PermissionRequiredMixin):
    def test_func(self):
        if isinstance(self.get_object(), Article):
            return self.request.user in self.get_object().authors.all()

# Create your views here.
def index(request, category=0):
    if category == 0:
        articles = Article.objects.all().order_by('-id')
    else:
        articles = Article.objects.filter(category=category).order_by('-id')
        category = Category.objects.get(id__exact=category)

    context = {
        'title': 'List of Articles',
        'articles': articles,
        'category': category
    }

    return render(request, 'pages/article_list.html', context)

def bad_index(request, category=1):
    articles = Article.objects.all().order_by('-id')
    category = Category.objects.get(id__exact=category)

    context = {
        'title': 'List of Articles',
        'articles': articles,
        'category': category
    }

    return render(request, 'pages/article_list_bad.html', context)

class CreateArticle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'pages/article_create.html'
    fields = ['title', 'category', 'short_desc', 'text', 'thumbnail', 'video']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    


class UpdateArticle(LoginRequiredMixin, ArticleAuthorMixin, UpdateView):
    model = Article
    template_name = 'pages/article_update.html'
    fields = ['title', 'category', 'short_desc', 'text', 'thumbnail', 'video']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context



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
    comments = Comment.objects.filter(article=article).order_by('-id')

    context = {
        'article': article,
        'comments': comments
    }

    return render(request, 'pages/article_detail.html', context)

def article_comment(request, articleid):
    article = Article.objects.get(id__exact=articleid)
    comments = Comment.objects.filter(article=article).order_by('-id')
    
    context = {
        'comments': comments,
        'article': article
    }

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                
                user = request.user
                comment_text = form.cleaned_data['comment_text']
                article=Article.objects.get(id__exact=articleid)

                comment = Comment.objects.create(user=user, article=article, comment_text=comment_text)
            else:
                print(form.errors)
    return render(request, 'partials/comments.html', context)

def delete_comment(request, articleid, commentid):
    article = Article.objects.get(id__exact=articleid)
    comments = Comment.objects.filter(article=article).order_by('-id')
    
    context = {
        'comments': comments,
        'article': article
    }

    # Delete horrible comment
    comment = Comment.objects.get(id__exact=commentid)

    if request.user == comment.user:
        comment.delete()

    return render(request, 'partials/comments.html', context)

def delete_article(request, slug):
    if request.user.has_perm('article.change_article'):
        article_title = Article.objects.filter(slug__exact=slug, authors=request.user)
        if article_title:
            article_title.delete()
        else:
            article_detail(request, slug)
    return HttpResponseRedirect(reverse('article:article_list'))

def article_item(request, articleid):
    article = Article.objects.get(id__exact=articleid)

    context = {
        'article': article
    }

    return render(request, 'partials/article_card.html', context)
