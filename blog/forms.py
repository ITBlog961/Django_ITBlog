from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категорія не вибрана'

    class Meta:
        model = Articles
        fields = ['title', 'content', 'photo', 'cat']
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-input'}),
            'content': forms.Textarea(attrs = {'cols': 60, 'rows': 10})
            }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
