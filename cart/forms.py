from django import forms
from .models import Order
from common.mixins import OptionalFormFieldsMixin


class BaseOrderForm(OptionalFormFieldsMixin, forms.ModelForm):
    optional_fields = ["apartment_building", "notes"]

    class Meta:
        model = Order
        exclude = ["user", "created_on", "number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label

        self.apply_placeholders(self)


class OrderForm(BaseOrderForm):
    agree_with_terms_of_use = forms.BooleanField(
        required=True, label="Запознат съм и съм съгласен с правила и условия на сайта."
    )

    def clean_agree_with_terms_of_use(self):
        agreed = self.cleaned_data.get("agree_with_terms_of_use")
        if not agreed:
            raise forms.ValidationError(
                "Трябва да се съгласите с правилата на сайта, преди да поръчате"
            )

        return agreed
