from django import forms
from .models import Order
from common.mixins import OptionalFormFieldsMixin


class BaseOrderForm(OptionalFormFieldsMixin, forms.ModelForm):
    optional_fields = ["apartment_building"]

    class Meta:
        model = Order
        exclude = ["user", "created_on"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = field_name.title().replace("_", " ")

        self.apply_placeholders(self)


class OrderForm(BaseOrderForm):
    save_information = forms.BooleanField(
        initial=False,
        required=False,
        label="Запази/Поднови информацията за бъдещи поръчки",
    )


class EditSavedCheckoutInformationForm(BaseOrderForm):
    pass
