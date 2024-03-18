from django import forms

from app.models import Product


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(choices=Product.Categories.choices, widget=forms.Select())
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'investment',
            'brand',
            'category',
            'image',
            'available',
        ]

