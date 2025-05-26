from django import forms
from blog_app.models.user import CustomUser


class UserProfile(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_image']