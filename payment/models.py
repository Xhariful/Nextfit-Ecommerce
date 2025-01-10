from django.db import models

# Create your models here.
class ShippingAddress(models.Model):
    TYPE = (
        ('Inside Dhaka', 'Inside Dhaka'),
        ('Outside Dhaka', 'Outside Dhaka'),
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    order_note = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE)
    address = models.TextField()

    def __str__(self):
        return f"Id:{self.id}, Name:{self.name}, Address:{self.address}"

# Create your models here.
