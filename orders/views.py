# orders/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import messages  # ✅ messages ব্যবহার

from products.models import Product
from .models import Order, OrderItem


def _get_cart(request):
    return request.session.get("cart", {})


def _cart_items_and_subtotal(request):
    cart = _get_cart(request)
    items = []
    subtotal = Decimal("0.00")

    for pid, data in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        qty = int(data.get("quantity", 1)) if isinstance(data, dict) else int(data)
        unit_price = product.price
        line_total = unit_price * qty
        subtotal += line_total
        items.append({
            "product": product,
            "qty": qty,
            "unit_price": unit_price,
            "line_total": line_total
        })
    return items, subtotal


@require_http_methods(["GET", "POST"])
def checkout(request):
    items, subtotal = _cart_items_and_subtotal(request)

    # ✅ কার্ট খালি থাকলে checkout করা যাবে না
    if request.method == "GET":
        if not items:
            messages.warning(request, "Your cart is empty. Add some products first.")
            return redirect("cart:detail")
        return render(request, "orders/checkout.html", {"items": items, "subtotal": subtotal})

    # POST
    if not items:
        messages.warning(request, "Your cart is empty. Add some products first.")
        return redirect("cart:detail")

    customer_name = request.POST.get("customer_name", "").strip()
    customer_mobile = request.POST.get("customer_mobile", "").strip()
    customer_email = request.POST.get("customer_email", "").strip()
    customer_address = request.POST.get("customer_address", "").strip()

    if not customer_name or not customer_mobile or not customer_address:
        return render(request, "orders/checkout.html", {
            "items": items,
            "subtotal": subtotal,
            "error": "Name, Mobile এবং Address আবশ্যক।",
            "customer_name": customer_name,
            "customer_mobile": customer_mobile,
            "customer_email": customer_email,
            "customer_address": customer_address,
        })

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total_price=subtotal,
        status="pending",
        customer_name=customer_name,
        customer_mobile=customer_mobile,
        customer_email=customer_email or None,
        customer_address=customer_address,
        created_at=timezone.now(),
    )

    for it in items:
        OrderItem.objects.create(
            order=order,
            product=it["product"],
            quantity=it["qty"],
            unit_price=it["unit_price"],
            line_total=it["line_total"],
        )

    # কার্ট খালি করো
    request.session["cart"] = {}
    request.session.modified = True

    return redirect("orders:success", order_id=order.id)


def my_orders(request):
    if request.user.is_authenticated:
        qs = Order.objects.filter(user=request.user).order_by("-created_at")
    else:
        qs = Order.objects.all().order_by("-created_at")[:10]
    return render(request, "orders/my_orders.html", {"orders": qs})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "orders/order_detail.html", {"order": order})


def success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "orders/success.html", {"order": order})
