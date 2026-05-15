# api/urls.py

from django.urls import path, include
from product.views import ProductImageViewSet, ProductViewSet, CategoryViewSet , ReviewViewSet
from order.views import CartViewSet , CartItemViewSet, OrderViewSet
from rest_framework_nested import routers


# DRF router ব্যবহার করে সব রাউট তৈরী করা হচ্ছে
router =routers.DefaultRouter()
router.register(r'products', ProductViewSet , basename='products')  # basename যুক্ত করা হয়েছে
router.register(r'categories', CategoryViewSet)
router.register(r'carts', CartViewSet , basename='carts')  # basename যুক্ত করা হয়েছে
router.register(r'orders', OrderViewSet , basename='orders')

product_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
product_router.register(r'reviews', ReviewViewSet, basename='product-reviews')
cart_router = routers.NestedDefaultRouter(router , r'carts' , lookup='cart')
cart_router.register(r'items' , CartItemViewSet , basename = 'cart-item' )
product_router.register(r'images', ProductImageViewSet, basename='product-images')


urlpatterns = [
    path('', include(router.urls)),  # সব URL রাউটারের মাধ্যমে manage হবে
    path('', include(product_router.urls)),  # Nested URL রাউটারের মাধ্যমে manage হবে
    path('' , include(cart_router.urls)),
    path('auth/', include('djoser.urls')),  # Djoser auth endpoints
    path('auth/', include('djoser.urls.jwt')),  # Djoser JWT endpoints
]
 