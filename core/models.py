from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 
# Create your models here.
        
class Website(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='web-logo')
    location = models.URLField(max_length=30, blank=True, null=True)
            
        
    def __str__(self):
                return self.name
            
    class Meta:
                ordering = ["name"]
                verbose_name = "Website"
                verbose_name_plural = "Website"

                
class WebsitePhone(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='website_phone')
    phone = models.CharField(max_length=30)
        
    def _str_(self):
        return f"Website {self.website}, Id #{self.id}"
            
    class Meta:
        ordering = ["phone"]
        verbose_name = "Website Phone"
        verbose_name_plural = "Website Phones"
        
class WebsiteEmail(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='website_email')
    email = models.EmailField()
        
    def _str_(self):
        return f"Website {self.website}, Id #{self.id}"
         
    class Meta:
        ordering = ["email"]
        verbose_name = "Website Email"
        verbose_name_plural = "Website Emails"
        
        
class WebsiteAddress(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='website_address')
    address = models.TextField()
        
    def _str_(self):
        return f"Website {self.website}, Id #{self.id}"
         
    class Meta:
        ordering = ["address"]
        verbose_name = "Website Address"
        verbose_name_plural = "Website addresses"
        
class ContactUs(models.Model):
    name = models.CharField(max_length=100)  # Example field
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField()
        
    def __str__(self):
        return self.name
            
        
        
        
        
class AboutUs(models.Model):
    description = RichTextUploadingField()
        
    def __str__(self):
        return str(self.id)
        
    class Meta:
        ordering = ["-id"]
        verbose_name = "AboutUs"
        verbose_name_plural = "AboutUses"
        
        
        
        
        
class Vission(models.Model):
            description = RichTextUploadingField () 
        
            def __str__(self):
                return str(self.id)
            
            class Meta:
                ordering = ["-id"]
                verbose_name = "Vission"
                verbose_name_plural = "Vissions"
            
        
class Mission(models.Model):
            description = RichTextUploadingField () 
        
            def __str__(self):
                return str(self.id)
            
            class Meta:
                ordering = ["-id"]
                verbose_name = "Mission"
                verbose_name_plural = "Missions"
            
        
class TermsCondition(models.Model):
    description =RichTextUploadingField() 
           
        
    def __str__(self):
        return str(self.id)
            
    class Meta:
        ordering = ["-id"]
        verbose_name = "TermsCondition"
        verbose_name_plural = "TermsConditions"
            
        
class PrivacyPolicy(models.Model):
    description =RichTextUploadingField() 
        
    def __str__(self):
        return str(self.id)
            
    class Meta:
        ordering = ["-id"]
        verbose_name = "privacypolicy"
        verbose_name_plural = "privacypolicys"