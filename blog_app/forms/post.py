from django import forms
from blog_app.models.post import Post


class Post(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas. Existing tags will be used, new tags will be created."
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags']
        widgets = {
            'content': forms.Textarea(),
            'status': forms.Select(choices=Post.STATUS_CHOICES),
        }