from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.text import slugify
from user.models import CustomUser
from django.utils import timezone
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField 
from payment.models import ShippingAddress 


# The WebsiteInfo model will now include a foreign key to the Website model






from django.db import models

class Carousol(models.Model):
    roll = models.IntegerField(unique=True)  
    img = CloudinaryField('Carousol_image',blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Carousel {self.roll}"  

    class Meta:
        ordering = ["roll"]  
        verbose_name = "Carousol"
        verbose_name_plural = "Carousols"


class OfferBanner(models.Model):
    roll = models.IntegerField(unique=True)  
    name = models.CharField(max_length=200)
    img = CloudinaryField('banner-image',blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.roll}"  

    class Meta:
        ordering = ["roll"]  
        verbose_name = "offerbanner"
        verbose_name_plural = "offerbanners"



class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = ["name"]  
        verbose_name = "Color"
        verbose_name_plural = "Colors"
    



class Size(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]  
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    img = CloudinaryField('categories-image',blank=True, null=True)
    parent = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE, blank=True, null=True)
    is_verify = models.BooleanField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["name"]
        verbose_name = "ProductCategory"
        verbose_name_plural = "Product Categories"

class Brand(models.Model):
    name = models.CharField(max_length=255)
    img = CloudinaryField('brand-image',blank=True, null=True)
    is_verify = models.BooleanField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

class Product(models.Model):
    name = models.CharField(max_length=100)
    img = CloudinaryField('product-image',blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    parent_code = models.CharField(max_length=200,unique=True, null=True)
    description = RichTextField() 
    short_description = RichTextField() 
    details_description = RichTextField() 
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_verify = models.BooleanField()
    is_show = models.BooleanField(default=False)
    free_delivery = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs) 

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


    

class Variation(models.Model): 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    variation_code = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='varition')
    quantity = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Generate variation_code if not set
        if not self.variation_code:
            parent_code = self.product.parent_code if self.product else ""
            color_name = self.color.name if self.color else ""
            size_name = self.size.name if self.size else ""
            self.variation_code = f"{parent_code}-{color_name}-{size_name}"
        super(Variation, self).save(*args, **kwargs)


    def get_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price
    
    def discount_percentage(self):
        if self.discount_price and self.price:
            discount_amount = self.price - self.discount_price
            discount_percentage = (discount_amount / self.price) * 100
            return discount_percentage
        else:
            return 0

    class Meta:
        unique_together = ('product', 'size', 'color')
     
    def __str__(self):
        return f"Variation: {self.variation_code} - {self.size} - {self.color}"
    
class ProductImage(models.Model):
    img = CloudinaryField('product-images',blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Image {self.id} for {self.product.name}"
    
    class Meta:
        ordering = ["-id"]
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class WishList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,)
    used = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code



class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)  



    def total(self):
        if self.variation.discount_price:
            total = self.variation.discount_price * self.quantity
        else:
            total = self.variation.price * self.quantity
        return total
    


    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"), 
        ("On the way", "On the way"),
        ("Cancelled", "Cancelled"),  
        ("Complete", "Complete")  
    )
    PAYMENT_TYPE_CHOICES = (
        ("Cash on delivery", "Cash on delivery"),  
        ("Bkash", "Bkash"),
        ("Nagad", "Nagad"),
        ("Rocket", "Rocket")
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, related_name='order')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment = models.CharField(max_length=30, choices=PAYMENT_TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True) 
    ordered = models.BooleanField(default=False)  
    complete_date = models.DateTimeField(blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    shipping = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)

    def sub_total(self):
        sub_total = 0
        for i in self.items.all():
            sub_total += i.total()
        return sub_total 

    def shipping_charge(self, value="Inside Dhaka"):
        if value=="Inside Dhaka":
            total = 80
        else:
            total = 160
        return total

    def coupon_total(self):
        if self.coupon:
            return self.coupon.discount_price * self.sub_total() / 100
        else:
            return 0

    def total_amount(self):
        total = (self.sub_total() + self.shipping_charge(type))
        return total
    
    def get_due_amount(self):
        return self.amount - self.paid_amount
    


    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    class Meta:
        ordering = ["-ordered_date"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"




class Blog(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextUploadingField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    img = CloudinaryField('blog-image',blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "BlogComment"
        verbose_name_plural = "BlogComments"
    


class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    massage = RichTextField(max_length=255)
    date = models.DateField(auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    

    class Meta:
        ordering = ["full_name"]
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"


# class VariationManager(models.Manager):
#     def all(self):
#         return super(VariationManager, self).filter(is_active=True)

#     def sizes(self):
#         return self.all().exclude(size__isnull=True)

#     def colors(self):
#         return self.all().exclude(color__isnull=True)
    

# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
#     size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
#     variation_code = models.CharField(max_length=120, null=True, blank=True)
#     image_for_color = models.ImageField(upload_to='ColorImage', blank=True, null=True)
#     video_url = models.URLField(null=True, blank=True)
#     quantity = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)

#     objects = VariationManager()

#     def save(self, *args, **kwargs):
#         if not self.variation_code:
#             if self.color and self.size and self.product.parent_code:
#                 self.variation_code = f"{self.product.parent_code}-{self.size.name}-{self.color.name}"
#             elif self.size and self.product.parent_code:
#                 self.variation_code = f"{self.product.parent_code}-{self.size.name}"
#             elif self.color and self.product.parent_code:
#                 self.variation_code = f"{self.product.parent_code}-{self.color.name}"
#             else:
#                 self.variation_code = self.product.product_name
#         super().save(*args, **kwargs)

#     def _str_(self):
#         if self.color and self.size:
#             return f"Size -{self.size.name} and Color -{self.color.name}"
#         else:
#             return self.product.product_name