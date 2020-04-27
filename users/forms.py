from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class SearchForm(forms.Form):
    data = [
        ('全体', '全体'),
        ('友人のみ', '友人のみ')
    ]
    select = forms.ChoiceField(
        choices=data,
        widget=forms.TextInput(attrs={'placeholder': '検索ワード'})
    )
    keyword = forms.CharField(
        max_length=100,
        required=False
    )
