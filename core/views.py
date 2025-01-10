from django.shortcuts import render
from .models import *

# Create your views here.
def about_us(request):
    obj = AboutUs.objects.all()
    return render(request,'about.html',{'obj':obj})

def vission(request):
    vission = Vission.objects.all()
    return render(request,'vission.html',{'vission':vission})

def mission(request):
    mission = Mission.objects.all()
    return render(request,'vission.html',{'mission':mission})

def termscondition(request):
    obj = TermsCondition.objects.all()
    return render(request,'about.html',{'obj':obj})

def privacypolicy(request):
    obj = PrivacyPolicy.objects.all()
    return render(request,'about.html',{'obj':obj})