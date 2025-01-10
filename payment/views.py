from django.shortcuts import render, redirect, get_object_or_404
from store.models import Order, OrderItem, Product, Variation, Coupon
from django.contrib.auth.decorators import login_required
from .forms import ShippingAddressForm
from django.contrib import messages
from django.utils.timezone import now
from decimal import Decimal
from .models import ShippingAddress

# Create your views here.


def checkout(request):
    # Retrieve session cart and coupon data
    cart = request.session.get('cart', {})
    coupon_data = request.session.get('coupon', {})
    order = Order.objects.filter(user=request.user, ordered=False).last()
    products = Product.objects.filter(is_show=True)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # Save the shipping address
            shipping_address = form.save(commit=False)
            shipping_address.order = order
            shipping_address.save()

            # Get and validate the payment type
            payment_type = request.POST.get('payment_type')
            if payment_type not in dict(Order.PAYMENT_TYPE_CHOICES):
                messages.error(request, "Invalid payment type selected.")
                return redirect('checkout')

            # Create a new order if none exists
            if not order:
                order = Order.objects.create(
                    user=request.user,
                    status="Pending",
                    ordered=False
                )

            # Process cart items from the session
            total_price = Decimal(0)  # Initialize total price as Decimal
            for variation_id, item_data in cart.items():
                quantity = item_data.get('quantity', 0)
                if quantity <= 0:
                    messages.error(request, "Invalid quantity provided.")
                    return redirect('cart')

                try:
                    variation = get_object_or_404(Variation, id=variation_id)
                except Variation.DoesNotExist:
                    messages.error(request, "One of the products in your cart does not exist.")
                    return redirect('cart')

                # Ensure the variation has sufficient stock
                if variation.quantity < quantity:
                    messages.error(
                        request,
                        f"Insufficient stock for {variation.product.name} ({variation.color.name}, {variation.size.name})."
                    )
                    return redirect('checkout')

                # Calculate total price
                total_price += Decimal(variation.get_price()) * quantity

                # Create or update OrderItem
                order_item, created = OrderItem.objects.get_or_create(
                    product=variation.product,
                    variation=variation,
                    user=request.user,
                    ordered=False
                )
                order_item.quantity = quantity
                order_item.ordered = True
                order_item.save()

                # Add the order item to the order
                order.items.add(order_item)

                # Reduce stock for the variation
                variation.quantity -= quantity
                variation.save()

            # Apply coupon discount if available
            discount_amount = Decimal(0)
            applied_coupon = None
            if coupon_data:
                coupon_code = coupon_data.get('code')
                applied_coupon = get_object_or_404(Coupon, code=coupon_code)
                discount_amount = Decimal(coupon_data.get('discount_amount', '0'))
                total_price -= discount_amount

            # Add shipping charges based on the address type
            shipping_charge = Decimal(50.00) if shipping_address.type == "Inside Dhaka" else Decimal(99.00)
            total_price += shipping_charge

            # Update the order
            order.payment = payment_type
            order.status = "Pending"
            order.ordered = True
            order.shipping = shipping_address
            order.complete_date = now()
            order.amount = total_price  # Save the discounted total price
            order.due_amount = total_price  # Adjust this if partial payments are allowed
            order.coupon = applied_coupon  # Save the applied coupon
            order.save()

            # Clear the session cart and coupon
            request.session['cart'] = {}
            request.session['coupon'] = {}

            messages.success(request, "Checkout completed successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors in the form.")
            print(form.errors)

    # Build order items from session cart
    order_items = []
    for variation_id, item_data in cart.items():
        quantity = item_data.get('quantity', 0)
        try:
            variation = get_object_or_404(Variation, id=variation_id)
            order_items.append({
                'variation': variation,
                'quantity': quantity,
                'total_price': Decimal(variation.get_price()) * quantity
            })
        except Variation.DoesNotExist:
            continue

    # Calculate total price for display
    cart_total = sum(item['total_price'] for item in order_items)
    discount_amount = Decimal(coupon_data.get('discount_amount', '0')) if coupon_data else Decimal(0)
    shipping_charge = Decimal(50.00) if 'Inside Dhaka' in coupon_data else Decimal(99.00)
    final_total = cart_total - discount_amount + shipping_charge

    context = {
        'order': order,
        'order_items': order_items,
        'products': products,
        'cart_total': cart_total,
        'discount_amount': discount_amount,
        'shipping_charge': shipping_charge,
        'final_total': final_total,
    }
    return render(request, 'checkout.html', context)


@login_required


def apply_coupon(request):
    time = now()
    cart = request.session.get('cart', {})
    cart_total = sum(
        Decimal(item['price']) * item['quantity']
        for item in cart.values()
    )

    print("cart total ===============",cart_total)  
    coupon_data = request.session.get('coupon', {})

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, "Coupon does not exist.")
            return redirect('checkout')

        # Validate coupon dates
        if coupon.start_date > time or coupon.end_date < time:
            messages.error(request, "Invalid coupon.")
            return redirect('checkout')
        
        # Validate coupon quantity
        if coupon.used >= coupon.quantity:
            messages.error(request, "Coupon usage limit reached.")
            return redirect('checkout')

        # Calculate the discounted price
        if cart_total > 0:
            discount_amount = cart_total * (coupon.discount_price / 100)
            discounted_total = cart_total - discount_amount
            coupon_data = {
                'code': coupon.code,
                'discount_amount': str(discount_amount),
                'final_price': str(discounted_total),
            }
            request.session['coupon'] = coupon_data

            # # Update coupon usage and save
            # coupon.used += 1
            # coupon.save()
            messages.success(request, "Coupon applied successfully!")
        else:
            messages.error(request, "Cart total must be greater than zero to apply a coupon.")

        print("=============coupon data=======",coupon_data)
        return redirect('checkout')

    messages.error(request, "Invalid request method.")
    return redirect('checkout')






        # if coupon:
        #     if coupon.start_date <= now and coupon.end_date >= now and coupon.quantity > coupon.used:
                
        #         coupon.used += 1
        #         coupon.save()
        #         messages.success(request, "Coupon applied successfully")
        #         return redirect('checkout')
        #     else:
        #         messages.error(request, "Coupon is expired or not available")
        #         return redirect('checkout')
        # else:
        #     messages.error(request, "Coupon Doesn't Exist")
        #     return redirect('checkout')