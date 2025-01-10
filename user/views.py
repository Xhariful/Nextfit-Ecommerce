from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from .forms import CustomerRegistrationForm, VendorRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from .forms import *



# ===============Customer_Register=================
def customer_register(request):
    if request.method == 'POST':
        # print("check me i am here .")
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')  
    else:
        form = CustomerRegistrationForm()
    return render(request, 'user/customer_register.html', {'form': form})


# ===============Vendor_Register=================
def vendor_register(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        # print("check me i am here .", request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')  
    else:
        form = VendorRegistrationForm()
    return render(request, 'user/vendor_register.html', {'form': form})


# ===============Login_View=================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('home')
            else:
                return redirect('home') 
    return render(request, 'user/login.html')

    

# ===============Logout_View=================
def logout_view(request):
    logout(request)
    return redirect('login_view')




# ===============change_password=================
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('login_view')
        else:
            messages.error(request, 'Please correct the errors below.')
            return redirect('home')
        




# ===============user_deshboard_Views=================
def user_deshboard(request): 
    return render(request,'user/user-deshboard/user-deshboard.html')


def purchase_history(request): 
    return render(request,'user/user-deshboard/purchase-history.html')


def my_review(request): 
    return render(request,'user/user-deshboard/my-review.html')


def manage_profile(request): 
    user = CustomUser.objects.get(id=request.user.id)
    profile = Profile.objects.filter(user=user)
   
    

    return render(request,'user/user-deshboard/manage-profile.html',{
        'user':user,
        'profile':profile,
    })

def profile_edit(request):
    user = CustomUser.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, 'User & Profile Updated sucesfully!!')
        else:
            messages.error(request, 'Somthing went Wrong!')

    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateForm(instance=profile)

    return render(request,'user/user-deshboard/profile-edit.html',{
        'user_form': user_form,
        'profile_form': profile_form,
    })

def return_product(request): 
    return render(request,'user/user-deshboard/return-product.html')


def change_password_view(request): 
    return render(request,'user/user-deshboard/change-password.html')

