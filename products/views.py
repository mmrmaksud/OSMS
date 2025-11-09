from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Product List
def product_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        products = Product.objects.filter(category_id=selected_category)
        selected_category = int(selected_category)
    else:
        products = Product.objects.all()
        selected_category = None

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

# Category Filter (optional, can use query param)
def category_products(request, category_id):
    categories = Category.objects.all()
    products = Product.objects.filter(category_id=category_id)
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })

# Product Detail
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Related products
    related_products = []
    if product.category:
        related_products = product.category.products.exclude(id=product.id)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
