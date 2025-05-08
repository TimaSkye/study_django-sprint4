from django import forms

from .models import User, Post


class UserForm(forms.ModelForm):
    """Форма для работы с пользователями."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PostForm(forms.ModelForm):
    """Форма для работы с постами."""
    pub_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'location', 'category', 'image',
                  'pub_date']
