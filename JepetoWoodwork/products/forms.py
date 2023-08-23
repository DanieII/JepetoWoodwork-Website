from django import forms
from django.core.validators import MinValueValidator
from .models import Category, ProductReview


class ProductSearchForm(forms.Form):
    search_field = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Търси..."})
    )


class ProductFilterForm(forms.Form):
    min_price = forms.FloatField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={"placeholder": "Минимална"}),
        required=False,
    )
    max_price = forms.FloatField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={"placeholder": "Максимална"}),
        required=False,
    )

    def clean(self):
        super().clean()

        min_price, max_price = self.cleaned_data.get(
            "min_price"
        ), self.cleaned_data.get("max_price")
        if min_price and max_price:
            if min_price > max_price:
                raise forms.ValidationError(
                    "Минималната цена трябва да е по-малка от максималната!"
                )

        return self.cleaned_data


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)], initial=1, min_value=1
    )


class ProductReviewForm(forms.ModelForm):
    INITIAL_STARS = 1

    class Meta:
        model = ProductReview
        fields = ["stars", "review"]
        widgets = {
            "stars": forms.HiddenInput(attrs={"class": "stars-field"}),
            "review": forms.Textarea(
                attrs={"placeholder": "Вашият отзив", "class": "review-field"}
            ),
        }
