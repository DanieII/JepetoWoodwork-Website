from django.shortcuts import redirect


class ProhibitLoggedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class HandleReviewMessageMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stars = self.request.GET.get("stars", 1)
        message = self.request.GET.get("message", "")
        context["stars"] = stars
        context["message"] = message

        return context

    def form_valid(self, form):
        stars = self.request.POST.get("stars")
        message = self.request.POST.get("message")
        response = super().form_valid(form)

        if message:
            return redirect(
                self.get_success_url() + f"?stars={stars}&message={message}"
            )

        return response
