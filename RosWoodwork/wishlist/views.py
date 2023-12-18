from django.shortcuts import redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


@login_required
def handle_heart_button(request, slug):
    url = request.POST.get("redirect_to")

    if url:
        wishlist = request.user.wishlist
        product = Product.objects.get(slug=slug)

        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)

        wishlist.save()

        return redirect(url)

    return redirect("home")


class WishListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "wishlist/wishlist.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        wishlist = self.request.user.wishlist
        product_slugs = [p.slug for p in wishlist.products.all()]
        queryset = queryset.filter(slug__in=product_slugs)
        return queryset
