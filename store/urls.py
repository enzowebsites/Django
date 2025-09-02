# store/urls.py (partial, for register)
from .views import (
    home, product_detail, add_to_cart, view_cart, checkout, search, category_filter, register, user_orders,
    remove_from_cart, update_cart, purchase_complete
)
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:pk>/', update_cart, name='update_cart'),
    path('cart/', view_cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('purchase_complete/', purchase_complete, name='purchase_complete'),
    path('search/', search, name='search'),
    path('category/<int:category_id>/', category_filter, name='category_filter'),
    path('register/', register, name='register'),
    path('orders/', user_orders, name='user_orders'),
]