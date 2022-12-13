from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    text = forms.CharField(max_length=3000, required=True)
    slug = forms.SlugField(max_length=255)

class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=300)
    comment_id = forms.IntegerField(required=False) # In case a certain comment is to be edited perchance :o