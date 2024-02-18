from django.db import models
from django.urls import reverse
from accounts.models import User
from address.models import District, Province
from django.utils import timezone
from datetime import datetime , timedelta
from django.utils.safestring import mark_safe

 


def compute_default_to():
    return datetime.now() + timedelta(days=7)



class Request(models.Model): 
 
    CHOICES = (
        ('S', 'Self Use'),
        ('R', 'Resale'),
    ) 
    
    business_sector = models.ForeignKey('product.Category',null=True,on_delete=models.SET_NULL)
    district = models.ForeignKey('address.District', on_delete=models.SET_NULL , null=True)

    purpose = models.CharField(max_length=1, choices=CHOICES , default='M')
    content = models.CharField(max_length=500)
    product_name = models.CharField(max_length=100)
    image = models.ImageField(blank=True,upload_to='request/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    quantity = models.IntegerField(blank=True, null= True)
    created = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    show_contact_info = models.BooleanField(default=False)
    active_days = models.IntegerField(default=7)

    show = models.BooleanField(default=False)
 
    def __str__(self):
        return str(self.user)

    def expiring_date(self):
        return self.created+timedelta(days=self.active_days)

    def status(self):
        if self.created >= timezone.now()-timedelta(days=self.active_days):
            if self.approved:
                return mark_safe('<span class="badge bg-soft-success text-success mr-3">Active</span>')
            else:
                return mark_safe('<span class="badge bg-soft-warning text-warning mr-3">Waiting</span>')
        else:
            return mark_safe('<span class="badge bg-soft-danger text-danger mr-3">Expired</span>')

 

class HideRequest(models.Model):
    request = models.ForeignKey(Request,null=True, on_delete=models.CASCADE, related_name='hidden_request')
    seller = models.ForeignKey("vendor.Seller", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.seller)


    

