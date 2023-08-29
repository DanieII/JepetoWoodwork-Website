from .helper_functions import get_user_saved_checkout_information


class FillOrderFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial_values = {}
        saved_checkout_information_obj = get_user_saved_checkout_information(
            self.request
        )

        if saved_checkout_information_obj:
            order = saved_checkout_information_obj.order
            initial_values.update(
                {field.name: getattr(order, field.name) for field in order._meta.fields}
            )

        user_contacts = {
            "email": self.request.user.email,
            "phone_number": self.request.user.phone_number,
        }
        initial_values.update({k: v for k, v in user_contacts.items() if v})

        kwargs.update(initial=initial_values)

        return kwargs
