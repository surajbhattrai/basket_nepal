from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from helper import file_size 
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save, post_save , post_delete
from django.dispatch import receiver



class BlogCategory(MPTTModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['id']

    def get_absolute_url(self):
        return reverse("blog_category", kwargs={"slug":self.slug})

 

class Blog(models.Model):

    title = models.CharField(max_length=500)
    category = models.ForeignKey('BlogCategory',null=True,on_delete=models.SET_NULL)
    image = models.ImageField( upload_to='blog/',validators=[file_size])
    description = RichTextField(blank=True)

    slug = models.SlugField(null=True, unique=True,max_length=500)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)      
     
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("Blog")
        verbose_name_plural = ("Blogs")
        ordering = ("-published",)


    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug":self.slug})



@receiver(post_delete, sender=Blog)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Blog)
def pre_save_image(sender, instance, *args, **kwargs):
    if instance.pk: 
        try:
            old_img = Blog.objects.get(pk=instance.pk).image
        except Blog.DoesNotExist:
            return
        else:
            try:
                new_img = instance.image
                if old_img and old_img.url != new_img.url:
                    old_img.delete(save=False)
            except:
                pass






