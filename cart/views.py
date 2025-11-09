from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from decimal import Decimal

def _get_cart(request):
    cart = request.session.get("cart", {})
    request.session.setdefault("cart", cart)
    return cart

def add_to_cart(request, pid):
    product = get_object_or_404(Product, id=pid)
    cart = _get_cart(request)
    item = cart.get(str(pid), {"name": product.name, "price": float(product.price), "qty": 0})
    item["qty"] += 1
    cart[str(pid)] = item
    request.session.modified = True
    return redirect("cart:view_cart")

def remove_from_cart(request, pid):
    cart = _get_cart(request)
    cart.pop(str(pid), None)
    request.session.modified = True
    return redirect("cart:view_cart")

def view_cart(request):
    cart = _get_cart(request)
    subtotal = sum(Decimal(str(i["price"])) * i["qty"] for i in cart.values())
    return render(request, "cart/cart_detail.html", {"cart": cart, "subtotal": subtotal})
