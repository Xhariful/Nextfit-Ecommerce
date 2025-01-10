from django.urls import path
from.views import *

urlpatterns = [
    #path('website_list/', website_list, name='website_list'), 
    # path('website/<slug:slug>/', website_detail, name='website_detail'),
    path("about-us",about_us,name="about_us"),
    path("vission",vission,name="vission"),
    path("mission",mission,name="mission"),
    
    path("termscondition",termscondition,name="termscondition"),
    
    path("privacypolicy",privacypolicy,name="privacypolicy"),


    
    
]