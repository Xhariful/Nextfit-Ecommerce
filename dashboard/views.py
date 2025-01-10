from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.core.paginator import Paginator
from .forms import *
from core.models import *
from store.models import *
# Create your views here.
def dashboard_home(request):
    return render(request, 'dashboard/index.html')

def website_info_list(request):
    obj_list = Website.objects.all()

    paginator = Paginator(obj_list, 10)
    page_number = request.GET.get("page")
    query = paginator.get_page(page_number)
    
    return render(request, 'web-info/website-info-list.html', {'query': query, 'obj_list': obj_list})


def  website_info_add(request):
    return render(request, 'web-info/website-info-add.html')



#==================== coupon section ====================
def coupon_list(request):
    obj_list = Coupon.objects.all()  # Get all coupons
    paginator = Paginator(obj_list, 2)  # 10 items per page
    page_number = request.GET.get("page")  # Get the page number from the query string
    query = paginator.get_page(page_number)  # Get the page object
    return render(request, 'coupon/coupon-list.html', {'query': query, 'now': now()})

def coupon_add(request):
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm()
    return render(request, 'dashboard/full-form.html', {'form': form})

def coupon_edit(request, id):
    obj = Coupon.objects.get(id=id)
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm(instance=obj)
    return render(request, 'dashboard/full-form.html', {'form':form})

def coupon_delete(request, id):
    Coupon.objects.get(id=id).delete()
    return redirect('coupon_list')