# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    products = Product.objects.all().order_by("-id")
    categories = Category.objects.all()
    selected_category = None
    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
    })

def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category).order_by("-id")
    categories = Category.objects.all()
    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "selected_category": category.id,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {"product": product})
