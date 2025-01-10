from django.contrib import admin
from .models import *
# Register your models here.

class WebsitePhoneAdmin(admin.TabularInline):
    model = WebsitePhone
    extra = 1

class WebsiteEmailAdmin(admin.TabularInline):
    model = WebsiteEmail
    extra = 1

class WebsiteAddressAdmin(admin.TabularInline):
    model = WebsiteAddress
    extra = 1

class WebsiteAdmin(admin.ModelAdmin):
    inlines = [WebsitePhoneAdmin, WebsiteEmailAdmin, WebsiteAddressAdmin]

admin.site.register(Website, WebsiteAdmin)

admin.site.register(AboutUs)
admin.site.register(Vission)
admin.site.register(Mission)
admin.site.register(TermsCondition)
admin.site.register(PrivacyPolicy)