
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField 
from .models import *

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:   
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"
    


class Division(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:   
        ordering = ["name"]
        verbose_name = "Division"
        verbose_name_plural = "Divisions"
    
class District(models.Model):
    name = models.CharField(max_length=50, unique=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    class Meta:   
        ordering = ["name"]
        verbose_name = "District"
        verbose_name_plural = "Districts"
    

class SubDistrict(models.Model):
    name = models.CharField(max_length=50, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:   
        ordering = ["name"]
        verbose_name = "SubDistrict"
        verbose_name_plural = "SubDistricts"

    

# Create your models here.
class CustomUserManager(BaseUserManager): # don't integrate on dashboard
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.pop('email', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, **extra_fields)


    
class CustomUser(AbstractBaseUser, PermissionsMixin): # don't integrate on dashboard
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=60, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='customuser_set',  # Custom related name to avoid conflicts
    #     blank=True,
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='customuser_set',  # Custom related name to avoid conflicts
    #     blank=True,
    # )

    def __str__(self):
        return  self.email or self.phone or "Unnamed User"
    

    # def save(self, *args, **kwargs):
    #     if self.is_customer and self.is_vendor:
    #         raise ValueError("A user cannot be both a customer and a vendor.")
    #     super().save(*args, **kwargs)



class Profile(models.Model): # don't integrate on dashboard
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="sellerpicture", default='avatar.png')
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='profiles', blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='profiles', blank=True, null=True)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, related_name='profiles', blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.email or self.user.phone 

    class Meta:
        verbose_name_plural = "Profiles"




class VendorProfile(models.Model): # don't integrate on dashboard
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    img = CloudinaryField('vendorpicture-image',blank=True, null=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='vendordivition', blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='vendordistric', blank=True, null=True)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, related_name='vendorsubdistric', blank=True, null=True)
    post_code = models.CharField(max_length=150)
    address = RichTextField()
    company_name = models.CharField(max_length=250)
    website = models.URLField()
    update_at = models.DateField(auto_now=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.email or self.user.phone 

    class Meta:
        verbose_name_plural = "Profiles"
        



@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_vendor:
            # Create a VendorProfile for vendors
            VendorProfile.objects.create(user=instance)
        else:
            # Create a regular Profile for non-vendors
            Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        if hasattr(instance, 'vendorprofile'):
            instance.vendorprofile.save()

        # all code ok
                           

    


