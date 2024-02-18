from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum, Avg
from helper import unique_slug_generator,file_size , ImageField
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField 
from urllib.parse import urlparse ,parse_qs
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from accounts.models import User 
from vendor.models import Seller
from django.db.models.signals import pre_save, post_save , post_delete
from django.dispatch import receiver
from django.conf import settings




 
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',on_delete=models.SET_NULL)
    image = models.ImageField(blank=True,  upload_to='category/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['id']
 
    def get_absolute_url(self):
        if not self.parent:
            return reverse("products_listview", kwargs={"slug":self.slug})
        else:
            return reverse("category", kwargs={"slug":self.slug})

    def get_category_image(self):
        if self.image:
            return self.image.url
        else:
            pass
    
    def hero_images(self):
        return self.design.design_images.filter(hero_section=True)


    def store_images(self):
        return self.design.design_images.filter(store_section=True)
        

@receiver(post_delete, sender=Category)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Category)
def pre_save_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_img = Category.objects.get(pk=instance.pk).image
        except Category.DoesNotExist:
            return
        else:
            try:
                new_img = instance.image
                if old_img and old_img.url != new_img.url:
                    old_img.delete(save=False)
            except:
                pass

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
  
class Product(models.Model):

    # Basic Information
    title = models.CharField(max_length=500)
    brand = models.CharField(max_length=120, blank= True)
    price = models.BigIntegerField(null=True , blank=True)

    buisness_sector = models.ForeignKey('Category',null=True,on_delete=models.SET_NULL,related_name="product_sector")
    category = models.ForeignKey('Category',null=True,on_delete=models.SET_NULL,related_name="product_catgeory")
    sub_category = models.ForeignKey('Category',null=True,on_delete=models.SET_NULL,related_name="product_subcatgeory")
    sub_subcategory = models.ForeignKey('Category',null=True, blank=True,on_delete=models.SET_NULL,related_name="product_subsubcatgeory")

    #Images
    img = models.ImageField( upload_to='product/',validators=[file_size])
    img_second = models.ImageField(blank=True ,  upload_to='product/',validators=[file_size])
    img_third = models.ImageField(blank=True ,  upload_to='product/',validators=[file_size])
    img_forth = models.ImageField(blank=True ,  upload_to='product/',validators=[file_size])
    img_fifth = models.ImageField(blank=True ,  upload_to='product/',validators=[file_size])
    video = models.URLField(blank=True , null=True)

    # highlights
    hightlight_one = models.CharField(max_length=200, blank= True)
    hightlight_two = models.CharField(max_length=200, blank= True)
    hightlight_three = models.CharField(max_length=200, blank= True)
    hightlight_four = models.CharField(max_length=200, blank= True)
    hightlight_five = models.CharField(max_length=200, blank= True)

    hightlight_six = models.CharField(max_length=200, blank= True)
    hightlight_seven = models.CharField(max_length=200, blank= True)
    hightlight_eight = models.CharField(max_length=200, blank= True)
    hightlight_nine= models.CharField(max_length=200, blank= True)
    hightlight_ten = models.CharField(max_length=200, blank= True)
   
    #Description
    description = RichTextField(blank=True)
    specification = RichTextField(blank=True)

    slug = models.SlugField(null=True, unique=True,max_length=500)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    seller = models.ForeignKey(Seller, default=1, on_delete=models.CASCADE, related_name='seller_product')
    
    search_vector = SearchVectorField(null=True ,blank=True)

    is_active = models.BooleanField(default=False) 
    
    objects = models.Manager()
    active = ActiveProductManager()
     
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")
        ordering = ("-published",)

        indexes = [
            GinIndex(fields=['search_vector']),
        ] 

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug":self.slug})


    def get_video_id(self):
        u_pars = urlparse(self.video)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            return pth[-1] 



def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)
    
pre_save.connect(product_pre_save_receiver, sender=Product)  




@receiver(post_delete, sender=Product)
def post_save_product_image(sender, instance, *args, **kwargs):
    try:
        instance.img.delete(save=False)
        instance.img_second.delete(save=False)
        instance.img_third.delete(save=False)
        instance.img_forth.delete(save=False)
        instance.img_fifth.delete(save=False)
    except:
        pass



@receiver(pre_save, sender=Product)
def pre_save_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_img = Product.objects.get(pk=instance.pk).img
            old_img_second = Product.objects.get(pk=instance.pk).img_second
            old_img_third = Product.objects.get(pk=instance.pk).img_third
            old_img_forth = Product.objects.get(pk=instance.pk).img_forth
            old_img_fifth = Product.objects.get(pk=instance.pk).img_fifth
        except Product.DoesNotExist:
            return
        else:
            try:
                new_img = instance
                new_img_second = instance.img_second
                new_img_third = instance.img_third
                new_img_forth = instance.img_forth
                new_img_fifth = instance.img_fifth

                if old_img and old_img.url != new_img.url:
                    old_img.delete(save=False)

                if old_img_second and old_img_second.url != new_img_second.url:
                    old_img_second.delete(save=False)

                if old_img_third and old_img_third.url != new_img_third.url:
                    old_img_third.delete(save=False)

                if old_img_forth and old_img_forth.url != new_img_forth.url:
                    old_img_forth.delete(save=False)

                if old_img_fifth and old_img_fifth.url != new_img_fifth.url:
                    old_img_fifth.delete(save=False)
            except:
                pass


