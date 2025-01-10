from django.contrib import admin
from .models import *

# Register your models here.
class ProductImageAdmin(admin.TabularInline):
    model =  ProductImage
    extra = 1

class VariationAdmin(admin.TabularInline):
    model =  Variation
    extra = 1



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageAdmin, VariationAdmin]
    list_display = ('name', 'is_verify', 'is_show', 'free_delivery')
    list_filter = ('is_verify', 'is_show', 'free_delivery')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)







admin.site.register(Carousol)
admin.site.register(Variation)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(WishList)
admin.site.register(Coupon)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(ContactUs)
admin.site.register(OfferBanner)

