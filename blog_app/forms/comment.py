from django import forms
from blog_app.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'post', 'user', 'content']