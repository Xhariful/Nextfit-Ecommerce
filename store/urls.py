from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('product-details/<slug:slug>/', product_details, name='product_detail'),

    path('product-filter/', product_filter, name='product_filter'),
 


    path('free-delivery/', free_delivery, name='free_delivery'),
    path('contact-us/', contact_us, name='contact_us'),


    path('wishlist/<slug>', wishlist, name='wishlist'),
    path('delete-wish/<slug:slug>/', delete_wish, name='delete_wish'),


    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('remove-cart-item/', remove_cart_item, name='remove_cart_item'),
    path('cart-quantity-increment/', cart_quantity_increment, name="cart_quantity_increment"),
    path('cart-quantity-decrement/', cart_quantity_decrement, name="cart_quantity_decrement"),

    
      






      
    
]