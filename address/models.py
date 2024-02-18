from django.db import models
from vendor.models import Seller



class Province(models.Model):
    province = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.province

  
class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    district = models.CharField(max_length=100,  null=True)

    def __str__(self):
        return self.district
    
 

class Address(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    building = models.CharField(max_length=120 , blank=True , null=True)
    city = models.CharField(verbose_name="City/Town",max_length=50 , blank=True , null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL , null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL , null=True)

    def __str__(self):
        return 'Address of {} with id {}'.format(self.seller, self.id)


