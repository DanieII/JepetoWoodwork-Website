from django.contrib.auth.views import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from .forms import EditSavedCheckoutInformationForm, OrderForm
from products.models import Product
from .models import Order, OrderProduct, SavedCheckoutInformation
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .helper_functions import (
    get_cart_products,
    get_total_price,
    process_cart_quantity,
    get_user_saved_checkout_information,
)
from django.contrib import messages
from .mixins import FillOrderFormMixin


def add_to_cart(request, slug, quantity=1):
    url = request.POST.get("redirect_to")

    if url:
        cart = request.session.get("cart", {})
        product = Product.objects.get(slug=slug)
        current_filled_quantity = cart.get(slug, 0)

        if not product.pre_order:
            if (
                product.quantity <= 0
                or product.quantity - (current_filled_quantity + quantity) < 0
            ):
                messages.warning(request, f"{product.name} не е наличен продукт")
                return redirect(url)

        if not current_filled_quantity:
            cart[slug] = 0

        request.session["cart"] = process_cart_quantity(
            slug, product, quantity, cart, product.pre_order
        )

        return redirect(url)

    return redirect("home")


def cart(request):
    cart_products = get_cart_products(request.session)

    context = {
        "cart_products": cart_products,
        "total_price": get_total_price(cart_products),
    }
    return render(request, "cart/cart.html", context)


def decrease_quantity(request, slug):
    cart = request.session["cart"]
    cart_product_quantity = cart[slug]

    if cart_product_quantity > 1:
        cart_product_quantity -= 1
        cart[slug] = cart_product_quantity
        request.session["cart"] = cart
        request.session.save()

    return redirect(reverse("cart"))


def remove_product(request, slug):
    request.session["cart"].pop(slug)
    request.session.save()

    return redirect(reverse("cart"))


class CheckoutView(FillOrderFormMixin, LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("home")

    def handle_save_information(self, save, order):
        if save:
            saved_checkout_information = get_user_saved_checkout_information(
                self.request
            )
            message = "Информацията за поръчки е запазена"
            if saved_checkout_information:
                message = "Информацията за поръчки е подновена"
                saved_checkout_information.delete()

            SavedCheckoutInformation.objects.create(
                user=self.request.user,
                first_name=order.first_name,
                last_name=order.last_name,
                city=order.city,
                address=order.address,
                apartment_building=order.apartment_building,
                postal_code=order.postal_code,
                phone_number=order.phone_number,
                email=order.email,
                delivery_type=order.delivery_type,
            )

            messages.success(self.request, message)

    @property
    def user_has_products(self):
        return self.request.session.get("cart")

    def get(self, request, *args, **kwargs):
        if self.user_has_products:
            return super().get(request)
        return redirect("products")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        cart_products = get_cart_products(self.request.session)
        total_price = get_total_price(cart_products)

        context["cart_products"] = cart_products
        context["total_price"] = total_price

        return context

    def form_valid(self, form):
        if not self.user_has_products:
            return redirect("products")

        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        cart = self.request.session["cart"]
        for product_slug, quantity in cart.items():
            product = Product.objects.get(slug=product_slug)
            product.quantity -= quantity
            product.save()
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        self.request.session["cart"] = {}
        self.handle_save_information(self.request.POST.get("save_information"), order)

        messages.success(self.request, "Поръчката е запазена")

        return super().form_valid(form)


class SavedCheckoutInformationView(
    LoginRequiredMixin, SuccessMessageMixin, FillOrderFormMixin, UpdateView
):
    model = SavedCheckoutInformation
    form_class = EditSavedCheckoutInformationForm
    template_name = "users/saved-checkout-information.html"
    success_url = reverse_lazy("saved_checkout_information")
    success_message = "Информацията за поръчки е подновена"

    def dispatch(self, request, *args, **kwargs):
        self.saved_checkout_information = get_user_saved_checkout_information(request)
        if not self.saved_checkout_information:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        return self.saved_checkout_information


@login_required
def delete_saved_checkout_information_view(request):
    checkout_information = get_user_saved_checkout_information(request)

    if not checkout_information:
        return redirect("home")

    checkout_information.delete()

    return redirect(reverse("user_details"))
