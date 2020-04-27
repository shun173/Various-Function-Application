from django import forms
from users.models import User
from ecapp.models import Sale


class ArticleForm(forms.Form):
    coentent = forms.CharField(max_length=500, widget=forms.Textarea)

    def __init__(self, user_id, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        user = User.objects.get(id=user_id)
        products = Sale.objects.filter(user=user)
        self.fields['products'] = forms.ChoiceField(
            choices=[('-', '-')] + [(product.name, product.name)
                                    for product in products]
        )
