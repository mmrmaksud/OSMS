# online_shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="products:product_list", permanent=False)),
    path("admin/", admin.site.urls),
    path("products/", include(("products.urls", "products"), namespace="products")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
