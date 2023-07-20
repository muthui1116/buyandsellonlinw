from django.urls import path
from .import views


urlpatterns = [
    path('marketplace/', views.marketplace, name='marketplace'),
    # CART IT SHOULD COME ABOVE THE VENDOR SLUG👇
    path('cart/', views.cart, name='cart'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    # ADD_TO_CART
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    # DECREASE CART
    path('decrease_cart/<int:item_id>/', views.decrease_cart, name='decrease_cart'),
    # DECREASE CART ITEM
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
]