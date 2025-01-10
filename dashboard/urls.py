from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard-home', dashboard_home, name='dashboard_home'),

    path('website-info-list', website_info_list, name='website_info_list'),
    path('website-info-add', website_info_add, name='website_info_add'),


    # coupon
    path('coupon-list', coupon_list, name='coupon_list'),
    path('coupon-add', coupon_add, name='coupon_add'),
    path('coupon-edit/<int:id>', coupon_edit, name='coupon_edit'),
    path('coupon-delete/<int:id>', coupon_delete, name="coupon_delete"),

]
