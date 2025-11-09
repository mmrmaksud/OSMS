from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')  # Show image in admin list

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
