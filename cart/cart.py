# cart/cart.py

class Cart:
    def __init__(self, request):
        # Initialize the cart by getting it from the session (or create an empty one if it doesn't exist)
        self.session = request.session
        cart = self.session.get('cart', {})
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        # Add or update a product in the cart
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_name': product.name,
                'price': str(product.price),  # Store as string to avoid issues with decimals
                'quantity': 0
            }
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Save the cart back to the session
        self.session['cart'] = self.cart
        self.session.modified = True

    def get_total_price(self):
        # Calculate the total price of the cart
        total_price = sum(
            item['quantity'] * float(item['price']) for item in self.cart.values()
        )
        return total_price
