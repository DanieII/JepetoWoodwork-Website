class OptionalFormFieldsMixin:
    optional_fields = []

    def apply_placeholders(self, *args, **kwargs):
        for field_name, field in self.fields.items():
            if field_name in self.optional_fields:
                placeholder = field.widget.attrs.get("placeholder", "")
                if placeholder:
                    placeholder += " (optional)"
                else:
                    placeholder = " (optional)"
                field.widget.attrs["placeholder"] = placeholder
