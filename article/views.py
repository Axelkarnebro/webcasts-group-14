from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from .models import Article
from article.forms import ArticleForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
    fields = ['title', 'text', 'slug']
    permission_required = ('article.add_article',)

    def form_valid(self, form):
        print("deez")
        response = super(CreateArticle, self).form_valid(form)
        form.instance.authors.add(self.request.user)
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

    context = {
        'article': article
    }

    return render(request, 'pages/article_detail.html', context)
