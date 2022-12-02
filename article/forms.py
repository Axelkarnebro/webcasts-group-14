from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    text = forms.CharField(max_length=3000, required=True)
    slug = forms.SlugField(max_length=255)