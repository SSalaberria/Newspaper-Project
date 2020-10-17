from django import forms

from articles.models import Comment


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=140, label='')

    class Meta:
        model = Comment
        exclude = ('article', 'author', )
