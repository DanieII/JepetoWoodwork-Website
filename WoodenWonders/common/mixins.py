class OptionalFormFieldsMixin:
    optional_fields = []

    def get_form(self):
        form = super().get_form()

        for field_name, field in form.fields.items():
            if field_name in self.optional_fields:
                placeholder = field.widget.attrs.get("placeholder", "")
                if placeholder:
                    placeholder += " (optional)"
                else:
                    placeholder = " (optional)"
                field.widget.attrs["placeholder"] = placeholder

        return form
