from django import forms
from core.models import *
from store.models import *
from payment.models import *
from user.models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField


## =================== Coupon ====================
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'