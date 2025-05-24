from django import forms
from blog_app.models.comment import Comment


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'post', 'user', 'content']