from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Questionnaire


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class ProfileForm(forms.Form):
    username = forms.CharField(
        label='ユーザー名',
        max_length=20,
    )
    email = forms.EmailField(
        label='Eメールアドレス',
        max_length=50
    )
    zip_code = forms.CharField(
        label='郵便番号',
        max_length=7,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '数字７桁（ハイフンなし）'})
    )
    address = forms.CharField(
        label='住所',
        max_length=100,
        required=False
    )


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
