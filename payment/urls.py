from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', checkout, name="checkout"),
    path('apply_coupon/', apply_coupon, name="apply_coupon"),
]