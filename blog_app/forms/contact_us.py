from django import forms
from blog_app.models import ContactUsModel


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ['name', 'email', 'message']