from django import forms
from django.core.validators import MinValueValidator


class ProductSearchForm(forms.Form):
    search_field = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Търси..."})
    )


class ProductSortForm(forms.Form):
    SORT_CHOICES = [
        ("low_to_high", "Цена (ниска към висока)"),
        ("high_to_low", "Цена (висока към ниска)"),
        ("new_to_old", "Дата (ново към старо)"),
        ("old_to_new", "Дата (старо към ново)"),
    ]
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=True)


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)], initial=1, min_value=1
    )
