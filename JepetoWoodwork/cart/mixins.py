from .helper_functions import get_user_saved_checkout_information


class FillOrderFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        saved_checkout_information_obj = get_user_saved_checkout_information(
            self.request
        )

        if saved_checkout_information_obj:
            kwargs.update(instance=saved_checkout_information_obj.order)

        initial_values = {
            "email": self.request.user.email,
            "phone_number": self.request.user.phone_number,
        }
        kwargs.update(initial=initial_values)

        return kwargs
