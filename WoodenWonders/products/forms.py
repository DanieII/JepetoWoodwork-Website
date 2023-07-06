from django import forms
from django.core.validators import MinValueValidator

from products.models import Category


class ProductFilterForm(forms.Form):
    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Select categories',
        required=False
    )
    min_price = forms.FloatField(
        validators=[
            MinValueValidator(1)
        ],
        widget=forms.NumberInput(attrs={'placeholder': 'Min'}),
        required=False
    )
    max_price = forms.FloatField(
        validators=[
            MinValueValidator(1)
        ],
        widget=forms.NumberInput(attrs={'placeholder': 'Max'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].choices = Category.get_choices()

    def clean(self):
        super().clean()
        min_price, max_price = self.cleaned_data.get('min_price'), self.cleaned_data.get('max_price')
        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError('The minimal price should be less than the max')

        return self.cleaned_data
