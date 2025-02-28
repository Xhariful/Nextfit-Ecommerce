from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["phone" ,"email", "date_joined"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["phone" ,"email", "password", "date_joined", "is_active", "is_staff", "is_vendor", "is_customer", "is_superuser",]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ["id","phone", "email", "is_superuser"]
    list_filter = ["is_superuser"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["full_name","phone"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_customer", "is_vendor", "is_superuser"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone" ,"email", "date_joined", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone", "email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
admin.site.register(VendorProfile)
admin.site.register(Country)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(SubDistrict)