from django import forms
from .models import Product


class AddToCartForm(forms.Form):
    def __init__(self, product_id, *args, **kwargs):
        super(AddToCartForm, self).__init__(*args, **kwargs)
        product = Product.objects.get(id=product_id)
        amount = product.amount
        self.fields['num'] = forms.IntegerField(
            label='数量',
            min_value=0,
            max_value=amount,
            required=True
        )


class SellForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'amount', 'image']
