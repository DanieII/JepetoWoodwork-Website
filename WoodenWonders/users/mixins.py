from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode


class ProhibitLoggedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class HandleQueryParamsFromLoginRequiredFormsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        given_fields = self.request.GET.get("login_required_form_fields")
        self.login_required_form_fields = {
            field: self.request.GET.get(field)
            for field in self.request.GET
            if field in given_fields
        }

        context["given_fields"] = given_fields
        context["login_required_form_fields"] = self.login_required_form_fields

        return context

    def form_valid(self, form):
        given_fields = self.request.POST.get("given_fields")
        login_required_form_fields = {
            field: self.request.POST.get(field)
            for field in self.request.POST
            if field in given_fields.split(",")
        }

        return redirect(
            self.get_success_url() + "?" + urlencode(login_required_form_fields)
        )


class HandleSendLoginRequiredFormInformationMixin:
    mixin_form = None
    fields = []
    additional_fields = {}

    def get_additional_fields(self):
        return {}

    def post(self, request, *args, **kwargs):
        form_instance = self.mixin_form(request.POST)
        if form_instance.is_valid():
            if not request.user.is_authenticated:
                fields_with_values = {}
                next_url = request.get_full_path()

                for field in self.fields:
                    fields_with_values[field] = form_instance.cleaned_data.get(field)

                parameters_in_query_format = urlencode(fields_with_values)
                fields_list = ",".join(self.fields)

                query_string = f"?next={next_url}&{parameters_in_query_format}&login_required_form_fields={fields_list}"

                login_url = reverse("login") + query_string

                return redirect(login_url)

            form_instance = form_instance.save(commit=False)

            additional_fields = self.additional_fields or self.get_additional_fields()
            for field, value in additional_fields.items():
                setattr(form_instance, field, value)

            for field in self.fields:
                field_value = request.POST.get(field)
                setattr(form_instance, field, field_value)

            form_instance.save()

        return redirect(self.get_success_url())
