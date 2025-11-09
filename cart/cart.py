from decimal import Decimal
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity <= 0:
                del self.cart[product_id]
            else:
                self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def get_items(self):
        items = []
        for product_id, data in self.cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = Decimal(data['price']) * data['quantity']
            items.append({'product': product, 'quantity': data['quantity'], 'subtotal': subtotal})
        return items

    def get_total(self):
        return sum(item['subtotal'] for item in self.get_items())
