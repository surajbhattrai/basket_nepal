from django.db import models
from accounts.models import User
from helper import file_size,unique_slug_generator
from django.urls import reverse
from datetime import datetime, timedelta
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_save , post_delete
from django.dispatch import receiver
from django.conf import settings
from django.templatetags.static import static
from django.core.exceptions import ValidationError


class StoreType(models.Model):
    name =  models.CharField(max_length=120)
    buisness_sector = models.ForeignKey('product.Category',null=True,on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)
        
    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Badge(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(upload_to='badges',validators=[file_size]) 

    def __str__(self):
        return self.title


class ActiveSellerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
 
  
class Seller(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=120)
    position = models.CharField(max_length=100)
    bio = models.CharField(max_length=300, blank=True)

    business_email = models.EmailField(max_length=254,blank=True, null=True)
    mobile = models.CharField(max_length=10 ,null=True , blank=True)
    telephone = models.CharField(max_length=10 ,null=True , blank=True)
    logo = models.ImageField(upload_to='seller/',validators=[file_size], blank=True)  
    registration_no = models.CharField(max_length=10)
    business_document = models.FileField(blank=True,upload_to='seller_doc',validators=[file_size])
    banner = models.ImageField(upload_to='seller/',validators=[file_size], blank=True ,null=True)  

    seller_type = models.ManyToManyField(StoreType, blank=True)
    category = models.ForeignKey('product.Category',blank=True, null=True,on_delete=models.SET_NULL,related_name="seller_category")

    basketnepal_pro = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=False) 
    featured = models.BooleanField(default=False) 
    ranking = models.IntegerField(default=3,validators=[MaxValueValidator(3),MinValueValidator(1)])
    badge = models.ManyToManyField(Badge, blank=True)
    slug = models.SlugField(unique=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active= ActiveSellerManager()
    
    def __str__(self):
        return str(self.title)
 
    def get_absolute_url(self):
        return reverse("storefront", kwargs={"slug":self.slug})
    
    def get_store_image(self):
        if self.logo:
            return self.logo.url
        else:
            return static('images/placeholder/img2.jpg')
 
    # def leads_left(self):
    #     limit = self.seller_package.lead_limit
    #     leads , created = Leads.objects.get_or_create(seller=self)
    #     used = LeadItems.objects.filter(leads=leads,created__gte=datetime.now()-timedelta(days=1)).count()
    #     return limit-used ;



@receiver(post_delete, sender=Seller)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.logo.delete(save=False)
        instance.banner.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Seller)
def pre_save_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_img = Seller.objects.get(pk=instance.pk).logo
            old_banner = Seller.objects.get(pk=instance.pk).banner
        except Seller.DoesNotExist:
            return
        else:
            try:
                new_img = instance.icon
                new_banner = instance.banner

                if old_img and old_img.url != new_img.url:
                    old_img.delete(save=False)

                if old_banner and old_banner.url != new_banner.url:
                    old_banner.delete(save=False)
            except:
                pass


def seller_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)
pre_save.connect(seller_pre_save_receiver, sender=Seller)

 

class SocialContact(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    facebook = models.URLField(max_length=100 ,null=True , blank=True)
    instagram = models.URLField(max_length=100 ,null=True , blank=True)

    def __str__(self):
        return str(self.seller)


class SellerPages(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='seller/pages',validators=[file_size], blank=True)
    title = models.CharField(max_length=120)
    content = RichTextField(blank=True)
    slug = models.SlugField(unique=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    list_as_item = models.BooleanField(default=False)
    show_on_frontpage = models.BooleanField(default=False)  

    def __str__(self):
        return str(self.seller)

    def get_absolute_url(self):
        return reverse("seller_page_detail", kwargs={"slug":self.slug})


def sellerpage_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)
    
pre_save.connect(sellerpage_pre_save_receiver, sender=SellerPages)

  
class StoreGallery(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='seller/gallery',validators=[file_size])  
    
    def __str__(self):
        return str(self.seller)        


@receiver(post_delete, sender=StoreGallery)
def post_save_gallay_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=StoreGallery)
def pre_save_gallary_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_img = StoreGallery.objects.get(pk=instance.pk).image
        except StoreGallery.DoesNotExist:
            return
        else:
            try:
                new_img = instance.image
                if old_img and old_img.url != new_img.url:
                    old_img.delete(save=False)
            except:
                pass