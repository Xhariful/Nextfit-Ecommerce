from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt 

from .models import Variation
import uuid
# All viwes
# Create your views here.
def home(request):
    carousol = Carousol.objects.filter(roll__gt=0).order_by('roll')
    banner = OfferBanner.objects.filter(roll__gt=0).order_by('roll')
    product = Product.objects.all()
    categories = ProductCategory.objects.filter(is_verify=True)
    # if 'cart' in request.session:
    #     del request.session['cart']
        # del request.session['coupon']

    context = {
        "product":product,
        "carousol":carousol,
        "banner":banner,
        "categories":categories,
    }
    return render(request, 'index.html', context)






from django.http import JsonResponse
import json

def product_details(request, slug):
    query = get_object_or_404(Product, slug=slug)
    product = Product.objects.filter(category=query.category)
    variations = Variation.objects.filter(product=query)
    variations_with_size = variations.filter(size__isnull=False)

    variations_data = [
        {
            "id": variation.id,
            "price": float(variation.price) if variation.price is not None else 0.0,
            "discount_price": float(variation.discount_price) if variation.discount_price is not None else 0.0,
            "size": variation.size.name if variation.size else "N/A",  # Default to "N/A" if None
            "color": variation.color.name if variation.color else "N/A",  # Default to "N/A" if None
            "variation_code": variation.variation_code,
            "quantity": variation.quantity,
        }
        for variation in variations
    ]
    print(variations_data)
    return render(request, 'product-details.html', {
        'query': query,
        'product': product,
        'variations_with_size': variations_with_size,
        'variations_json': json.dumps(variations_data),  # Pass JSON to the template
    })




def get_descendants(category):
    descendants = []
    children = ProductCategory.objects.filter(parent=category)
    for child in children:
        descendants.append(child)
        descendants.extend(get_descendants(child))
    return descendants

def product_filter(request):
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')


    # Fetch categories
    products = Product.objects.filter(is_show=True)
    categories = ProductCategory.objects.filter(parent=None, is_verify=True)
    # print("all  categories============================", categories)
    parent_categories = ProductCategory.objects.filter(parent__isnull=True)
    # print("all parents categories============================", parent_categories)
    brands = Brand.objects.filter(is_verify=True)
    # print("all brands============================", brands)

    selected_category = None
    if selected_category_id:
        selected_category = get_object_or_404(ProductCategory, id=selected_category_id)
        descendants = get_descendants(selected_category)
        products = products.filter(category__in=[selected_category] + descendants)
        
    selected_brand = None
    if selected_brand_id:
        selected_brand = get_object_or_404(Brand, id=selected_brand_id)
        products = products.filter(brand=selected_brand)
        print("=================",products)


    if min_price or max_price:
        variations = Variation.objects.all()
        if min_price:
            variations = variations.filter(price__gte=min_price)
        if max_price:
            variations = variations.filter(price__lte=max_price)
        products = products.filter(varition__in=variations).distinct()
        print("price product=================",products)



    return render(request, 'product-filter.html', {
        'categories': categories,
        'selected_category': selected_category,
        'parent_categories': parent_categories,
        'products': products,
        'selected_brand': selected_brand,
        'brands': brands,
        'min_price': min_price,
        'max_price': max_price,
    })


def add_to_cart(request):
    if request.method == "POST":
        selected_size = request.POST.get('size')
        selected_color = request.POST.get('color')
        product_id = request.POST.get('product_id')
        try:
            quantity = int(request.POST.get('quantity'))
        except (TypeError, ValueError):
            return JsonResponse({"error": "Quantity must be a positive integer."}, status=400)

        if not product_id or quantity <= 0:
            return JsonResponse({"error": "Product ID and valid quantity are required."}, status=400)

        size = None
        color = None
        if selected_size:
            size = get_object_or_404(Size, name=selected_size)
        if selected_color:
            color = get_object_or_404(Color, name=selected_color)

        try:
            product = get_object_or_404(Product, id=product_id)
            # if size and color:
            variation = get_object_or_404(
                Variation,
                product=product,
                size=size,
                color=color,
                quantity__gte=quantity
            )
            # elif size:
            #     variation = get_object_or_404(
            #         Variation,
            #         product=product,
            #         size=size,
            #         colour=color,
            #         quantity__gte=quantity
            #     )
            # elif color:
            #     variation = get_object_or_404(
            #         Variation,
            #         product=product,
            #         size=size,
            #         colour=color,
            #         quantity__gte=quantity
            #     )
            # else:
            #     variation = get_object_or_404(
            #         Variation,
            #         product=product,
            #         size=size,
            #         colour=color,
            #         quantity__gte=quantity
            #     )

            # Using variation ID as key for cart
            variation_id = str(variation.id)
            cart = request.session.get('cart', {})
            # print("===============",variation)
            # print("===============",size)
            # print("===============",color)
            if variation_id in cart:
                cart[variation_id]['quantity'] += quantity
            else:
                # Add new item to cart
                cart[variation_id] = {
                    "product_id": product.id,
                    "variation_id": variation.id,
                    "product_name": product.name,
                    "img": product.img.url if product.img else None,
                    "size": size.name if size else None,
                    "color": color.name if color else None,
                    "quantity": quantity,
                    "price": float(variation.get_price()),
                }

            # Save the updated cart back to session
            request.session['cart'] = cart
            request.session.modified = True
             # Calculate the total price
            total_price = calculate_cart_total(request)

            # Add total price to the success message (or return in response)
            messages.success(request, f"Item successfully added to cart. Total Price: ${total_price:.2f}")

        except Exception as e:
            messages.error(request, f"Error {e}")
        # Calculate the total price and pass to the context

    return redirect('product_detail', product.slug)


def calculate_cart_total(request):
    cart = request.session.get('cart', {})

    # Initialize total price to 0
    total_price = 0

    for item in cart.values():
        # Multiply the price by the quantity of each item
        total_price += item['price'] * item['quantity']

    return total_price

        # print('==================== Product name:', product.name)
        # print('==================== Product Quantity:', variation.quantity)
        # print('=============== Size:', size if size else "N/A")
        # print('=============== Color:', color if color else "N/A")
        # print('=============== Quantity:', quantity)
        # print('================= Product ID:', product_id)
        # print(f"Selected Variation ID: {variation.id}")
        
def cart_quantity_increment(request):
    if request.method == "POST":
        try:
            product_id = int(request.POST.get('product_id'))
            variation_id = int(request.POST.get('variation_id'))
            product = Product.objects.get(id=product_id)

        except (TypeError, ValueError):
            messages.error(request, "Invalid product or variation ID.")
            return redirect('cart')

        # Get the cart from session
        cart = request.session.get("cart", {})

        variation_id_str = str(variation_id)  
        if variation_id_str in cart:
            try:
                variation = get_object_or_404(Variation, id=variation_id)
                if cart[variation_id_str]["quantity"] < variation.quantity:
                    cart[variation_id_str]["quantity"] += 1
                    request.session["cart"] = cart
                    request.session.modified = True
                    messages.success(request, "Quantity increased.")
                else:
                    messages.error(request, "No more stock available for this item.")
            except Exception as e:
                messages.error(request, "Error updating cart. Please try again.")
        else:
            messages.error(request, "Item not found in cart.")

        return redirect('product_detail', product.slug)



def cart_quantity_decrement(request):
    if request.method == "POST":
        try:
            product_id = int(request.POST.get('product_id'))
            variation_id = int(request.POST.get('variation_id'))
            product = Product.objects.get(id=product_id)

        except (TypeError, ValueError):
            messages.error(request, "Invalid product or variation ID.")
            return redirect('cart')

        # Get the cart from session
        cart = request.session.get("cart", {})

        variation_id_str = str(variation_id) 
        if variation_id_str in cart:
            if cart[variation_id_str]["quantity"] > 1:
                cart[variation_id_str]["quantity"] -= 1
                request.session["cart"] = cart
                request.session.modified = True
                messages.success(request, "Quantity decreased.")
            else:
                messages.error(request, "Cannot reduce quantity below 1.")
        else:
            messages.error(request, "Item not found in cart.")

        return redirect('product_detail', product.slug)



def remove_cart_item(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        variation_id = request.POST.get("variation_id")


        cart = request.session.get("cart", [])
        for item in cart:
            if (
                int(item) == int(variation_id) 
            ):
                # cart.pop(item)
                del cart[item]
                break
        # Save the updated cart back to the session
        request.session["cart"] = cart
        request.session.modified = True

        # Add a success message
        messages.success(request, "Item successfully removed from the cart.")

    return redirect('product_detail', product.slug)






def wishlist(request, slug):
    # Fetch the product using the slug
    product = get_object_or_404(Product, slug=slug)

    # Retrieve the cart from session, or create an empty cart
    wishlist = request.session.get('wishlist', {})

    # Add product to cart or update quantity
    if  slug not in wishlist:

        wishlist[slug] = {
            'name': product.name,
            'slug': product.slug,
            'img': product.img.url,
            'quantity': 1,
        }


        request.session['wishlist'] = wishlist
        messages.success(request, "Item successfully added to Wishlist.")
    else:
        messages.info(request, "Item already in wishlist.")
    # Save the cart back to the session
    

    # print("==================",wishlist)

    return redirect('home')

def delete_wish(request, slug):
    wishlist = request.session.get('wishlist', {})
    
    if slug in wishlist:
        del wishlist[slug]
        request.session['wishlist'] = wishlist
        request.session.modified = True
        messages.success(request, "Item removed from wishlist.")
    else:
        messages.error(request, "Item not found in wishlist.")
    
    return redirect('home') 



def free_delivery(request):
    free_delivery = Product.objects.filter(free_delivery=True)
    return render(request, 'free_delivery.html', {
        'free_delivery': free_delivery,
        })



















def contact_us(request):
    form = ContactUsForm() 
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        # print('i am success====',request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Somthing went Wrong!')
    return render(request,'contact-us.html', {'form':form})































































# def add_to_cart(request):
#     if request.method == "POST":
#         # Get data from the POST request
#         selected_size = request.POST.get('size')
#         selected_color = request.POST.get('color')
#         product_id = request.POST.get('product_id')
#         quantity = request.POST.get('quantity')

#         if not product_id or not quantity:
#             return JsonResponse({"error": "Product ID and quantity are required."}, status=400)
#         size = None
#         color = None
#         if selected_size:
#             size = get_object_or_404(Size, name=selected_size)
#         if selected_color:
#             color = get_object_or_404(Colour, name=selected_color)

#         try:
#             product = get_object_or_404(Product, id=product_id)
#             if size and color:
#                 variation = get_object_or_404(
#                     Variation,
#                     product=product,
#                     size=size,
#                     colour=color,
#                     quantity__gte=quantity
#                 )
#             elif size:
#                 variation = get_object_or_404(
#                     Variation,
#                     product=product,
#                     size=size,
#                     quantity__gte=quantity
#                 )
#             elif color:
#                 variation = get_object_or_404(
#                     Variation,
#                     product=product,
#                     colour=color,
#                     quantity__gte=quantity
#                 )
#             else:
#                 variation = get_object_or_404(
#                     Variation,
#                     product=product,
#                     quantity__gte=quantity
#                 )
#             print('==================== Product name:', product.name)
#             print('==================== Product Quantity:', variation.quantity)
#             print('=============== Size:', size if size else "N/A")
#             print('=============== Color:', color if color else "N/A")
#             print('=============== Quantity:', quantity)
#             print('================= Product ID:', product_id)
#             print(f"Selected Variation ID: {variation.id}")

#         except Exception as e:
#             return JsonResponse({
#                 "message": "Item successfully added to cart without size and color."
#             }, status=200)

#         return JsonResponse({
#             "message": "Item successfully added to cart."
#         }, status=200)

#     # If the request method is not POST, redirect to home
#     return redirect('home')
