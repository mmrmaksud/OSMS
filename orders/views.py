from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Order, OrderItem
from cart.cart import Cart
from .forms import OrderForm 


def _parse_cart(cart_dict):
    items = []
    subtotal = Decimal("0.00")

    for pid, val in cart_dict.items():
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
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['price'],
                    line_total=item['total_price']
                )
            cart.clear()
            return redirect('orders:success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})
