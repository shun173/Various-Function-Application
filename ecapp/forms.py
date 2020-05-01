from django import forms
from .models import Product


class AddToCartForm(forms.Form):
    num = forms.IntegerField(
        label='数量',
        min_value=1,
        required=True
    )


class PurchaseForm(forms.Form):
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


class SellForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'amount', 'image']
