# online_shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # Products app (main shop home)
    path("", include(("products.urls", "products"), namespace="products")),

    # Cart app
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),

    # Orders app (checkout, order confirm, etc.)
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),

    # Authentication (login/logout)
    path("accounts/", include("django.contrib.auth.urls")),
]

# Static and media files configuration
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
