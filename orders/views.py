# orders/views.py
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .models import Order, OrderItem


def _parse_cart(cart_dict):
    """
    cart_dict structure examples:
    {
        "12": {"quantity": 2},     # preferred
        "7": 1                     # legacy/int form
    }
    Returns: (items, subtotal)
      items = [(product, qty, unit_price, line_total), ...]
    """
    items = []
    subtotal = Decimal("0.00")

    for pid, val in cart_dict.items():
        # Support both {"quantity": x} and plain int
        if isinstance(val, dict):
            qty = int(val.get("quantity") or val.get("qty") or 1)
        else:
            qty = int(val)

        product = get_object_or_404(Product, pk=int(pid))
        unit_price = product.price
        line_total = unit_price * qty

        subtotal += line_total
        items.append((product, qty, unit_price, line_total))

    return items, subtotal


@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    # If cart is empty, go back to cart page
    if not cart:
        return redirect("cart:cart_detail")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        items, subtotal = _parse_cart(cart)

        # Create the Order
        order = Order.objects.create(
            user=request.user,
            full_name=name,
            phone=phone,
            address=address,
            total_amount=subtotal,
        )

        # Create each OrderItem
        for product, qty, unit_price, _line_total in items:
            # models.OrderItem has fields: order, product, quantity, price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=unit_price,  # unit price per item
            )

        # Clear cart
        request.session["cart"] = {}
        request.session.modified = True

        return redirect("orders:success", order_id=order.id)

    # GET: show a summary before confirming
    items, subtotal = _parse_cart(cart)
    detailed = [
        {"product": p, "qty": qty, "unit_price": unit, "line_total": line}
        for (p, qty, unit, line) in items
    ]
    return render(
        request,
        "orders/checkout.html",
        {"items": detailed, "subtotal": subtotal},
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Your template is orders/templates/orders/order_success.html
    return render(request, "orders/order_success.html", {"order": order})
