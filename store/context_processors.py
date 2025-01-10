from store.models import ProductCategory
from store.views import calculate_cart_total

def dynamic_data(request):
    con_categories = ProductCategory.objects.filter(parent=None, is_verify=True)
    con_cart = request.session.get('cart', {})
    con_coupon = request.session.get('coupon', {})
    count_cart = len(con_cart)
    con_wishlist = request.session.get('wishlist', {})
    count_wishlist = len(con_wishlist)
    con_total = calculate_cart_total(request)
    # print("cart save data============",con_cart)
    return {
        'con_categories':con_categories,
        'con_cart':con_cart,  
 

        'con_coupon':con_coupon,  
        'count_cart':count_cart,  

        'con_wishlist':con_wishlist,  
        'con_total':con_total,  
        'count_wishlist':count_wishlist,  
    }