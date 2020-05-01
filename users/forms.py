from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Questionnaire


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['evaluation', 'content']


DATA = [
    ('全体', '全体'),
    ('友人のみ', '友人のみ')
]


class SearchForm(forms.Form):
    select = forms.ChoiceField(
        choices=DATA,
    )
    keyword = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '検索ワード'})
    )
