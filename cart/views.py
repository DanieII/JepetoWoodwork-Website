from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order, OrderProduct
from products.models import Product
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .utils import get_products_with_quantities, send_email_to_admin


def cart_view(request):
    cart = request.session.get("cart", {})
    products_with_quantities = get_products_with_quantities(cart)
    context = {
        "cart_products": products_with_quantities,
        "total_price": sum(
            product.price * quantity
            for product, quantity in products_with_quantities.items()
        ),
    }

    return render(request, "cart/cart.html", context)


def add_to_cart_view(request, slug, quantity=1):
    redirect_url = request.POST.get("redirect_to") or "home"
    product = Product.objects.get(slug=slug)
    cart = request.session.get("cart", {})
    cart_product_quantity = cart.get(slug, 0)

    if not product.is_available:
        messages.warning(request, f"{product.name} не е наличен продукт")
        return redirect(redirect_url)

    if not cart_product_quantity:
        cart[slug] = cart_product_quantity

    cart[slug] += quantity
    request.session["cart"] = cart

    messages.success(request, f"{product.name} е добавен в количката")

    return redirect(redirect_url)


def decrease_quantity_view(request, slug):
    cart = request.session.get("cart", {})
    cart_product_quantity = cart.get(slug, 0)

    if cart_product_quantity > 1:
        cart_product_quantity -= 1
        cart[slug] = cart_product_quantity
        request.session["cart"] = cart

    return redirect(reverse("cart"))


def remove_product_view(request, slug):
    request.session.get("cart", {}).pop(slug, None)
    request.session.save()

    return redirect(reverse("cart"))


class CheckoutView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        cart = self.request.session.get("cart", {})
        if not cart:
            return redirect("cart")

        return super().dispatch(request, *args, **kwargs)

    def create_order(self, form, products_with_quantities):
        self.object = form.save()

        order_products = [
            OrderProduct(order=self.object, product=product, quantity=quantity)
            for product, quantity in products_with_quantities.items()
        ]
        OrderProduct.objects.bulk_create(order_products)

    def form_valid(self, form):
        cart = self.request.session.get("cart", {})
        if not cart:
            return redirect("cart")

        try:
            products_with_quantities = get_products_with_quantities(cart)
            self.create_order(form, products_with_quantities)
            self.request.session["cart"] = {}

            send_email_to_admin(self.request, self.object)
            messages.success(self.request, "Поръчката е изпратена")
        except Exception as e:
            messages.error(self.request, "Възникна грешка при обработката на поръчката")
            return redirect("cart")

        return super().form_valid(form)
