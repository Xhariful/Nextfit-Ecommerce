from django.urls import path
from .views import *
urlpatterns = [
    path('customer-register', customer_register, name='customer_register'),
    path('vendor-register', vendor_register, name='vendor_register'),
    path('logout-view', logout_view, name='logout_view'),
    path('login-view', login_view, name='login_view'),
    path('change-password', change_password, name='change_password'),


    # ==================user deshboard url===========================
    path('user_deshboard', user_deshboard, name='user_deshboard'),
    path('purchase-history', purchase_history, name='purchase_history'),
    path('my-review', my_review, name='my_review'),
    path('manage-profile', manage_profile, name='manage_profile'),
    path('return-product', return_product, name='return_product'),
    path('change-password-view', change_password_view, name='change_password_view'),
    path('profile-edit', profile_edit, name='profile_edit'),
    
    
]