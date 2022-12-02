from django import forms

class ArticleForm(forms.Form):
    Title = forms.CharField(max_length=50, required=True)
    Text = forms.CharField(max_length=3000, required=True)
    Slug = forms.SlugField(max_length=255)