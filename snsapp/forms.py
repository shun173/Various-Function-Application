from django import forms
from django.contrib.auth import get_user_model
from ecapp.models import Sale


class ArticleForm(forms.Form):
    content = forms.CharField(
        max_length=500,
        widget=forms.Textarea(
            attrs={'placeholder': '商品の評価を投稿する場合は商品を選択してください'})
    )

    def __init__(self, user_id, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        sales = Sale.objects.filter(user=user)
        products = []
        for sale in sales:
            product = sale.product
            products.append(product)
        self.fields['product'] = forms.ChoiceField(
            choices=[(None, '-')] + [(product.pk, product.name)
                                     for product in products],
            required=False
        )
