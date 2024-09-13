from django.contrib.auth.views import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order, OrderProduct, SavedCheckoutInformation
from products.models import Product
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .helper_functions import (
    get_cart_products,
    get_total_price,
    process_cart_quantity,
)
from django.contrib import messages
from django.contrib.auth.models import send_mail
from django.conf import settings
from django.utils.html import format_html


def add_to_cart(request, slug, quantity=1):
    url = request.POST.get("redirect_to")

    if url:
        products = Product.objects.all()
        product = products.get(slug=slug)
        cart = request.session.get("cart", {})
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


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("user_orders")

    def send_order_email(self, order):
        host_email = settings.EMAIL_HOST_USER
        order_details_url = reverse("admin:cart_order_change", args=[order.pk])
        link_url = self.request.build_absolute_uri(order_details_url)
        link_html = format_html('<a href="{}">Виж</a>', link_url)
        message = f"Нова поръчка е направена: {link_html}"

        try:
            send_mail(
                subject="Нова Поръчка",
                message=message,
                html_message=message,
                from_email=host_email,
                recipient_list=[host_email],
            )
        except:
            pass

    @property
    def user_has_products(self):
        return self.request.session.get("cart")

    def validate_cart(self):
        cart = self.request.session.get("cart")
        new_cart = cart.copy()
        valid = cart != {}

        if valid:
            products = Product.objects.all()
            for slug, quantity in cart.items():
                product = products.get(slug=slug)

                if not product.pre_order and (
                    not product.available or (product.quantity - quantity < 0)
                ):
                    new_cart.pop(slug)
                    valid = False

        self.request.session["cart"] = new_cart
        return valid

    def dispatch(self, request, *args, **kwargs):
        valid_cart = self.validate_cart()

        if valid_cart:
            return super().dispatch(request)

        messages.warning(
            self.request, "Празна количка или неналични продукти. Опитайте отново."
        )
        return redirect("cart")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        cart_products = get_cart_products(self.request.session)
        total_price = get_total_price(cart_products)

        context["cart_products"] = cart_products
        context["total_price"] = total_price

        return context

    def form_valid(self, form):
        if not self.user_has_products:
            return redirect("cart")

        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        cart = self.request.session["cart"]
        products = Product.objects.all()
        for product_slug, quantity in cart.items():
            product = products.get(slug=product_slug)

            if not product.pre_order:
                product.quantity -= quantity
                product.save()

            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        self.request.session["cart"] = {}

        messages.success(self.request, "Поръчката е запазена")
        self.send_order_email(order)

        return super().form_valid(form)
