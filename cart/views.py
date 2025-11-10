from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product

CART_SESSION_KEY = "cart"

def _get_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})

def cart_detail(request):
    cart = _get_cart(request)
    items = []
    subtotal = Decimal("0.00")
    for pid, data in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        qty = int(data.get("quantity", 1)) if isinstance(data, dict) else int(data)
        line_total = product.price * qty
        subtotal += line_total
        items.append({
            "product": product,
            "qty": qty,
            "unit_price": product.price,
            "line_total": line_total,
        })
    return render(request, "cart/cart_detail.html", {"items": items, "subtotal": subtotal})

@require_POST
def add(request, product_id):
    cart = _get_cart(request)
    pid = str(product_id)
    current = cart.get(pid, {"quantity": 0}) if isinstance(cart.get(pid), dict) else {"quantity": int(cart.get(pid, 0))}
    current["quantity"] = int(current.get("quantity", 0)) + 1
    cart[pid] = current
    request.session.modified = True
    return redirect("cart:cart_detail")

@require_POST
def remove(request, product_id):
    cart = _get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        request.session.modified = True
    return redirect("cart:cart_detail")
