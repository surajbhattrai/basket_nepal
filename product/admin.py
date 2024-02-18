from django.contrib import admin
from .models import Product , Category 
from mptt.admin import DraggableMPTTAdmin
from django.contrib import messages
from django.utils.translation import ngettext
from helper import ExportCsvMixin
from django.utils.safestring import mark_safe



 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin,ExportCsvMixin):
    date_hierarchy = 'published'
    list_display = ['title','store','category','sub_category','sub_subcategory','is_active']
    list_filter = ['published','updated']
    list_per_page = 40
    search_fields = ['title','description','seller__title','category__name']
    actions = ['make_active','export_as_csv']
    empty_value_display = 'N/A'

    readonly_fields = ["first_image","second_image","third_image","forth_image","fifth_image",'published','updated']

    fieldsets = (
        ("Basic Information", {
                "fields": ("title","slug", "price", "brand","seller","published","updated","is_active")
        }),

        ('Category', {
            'fields': ('buisness_sector','category', 'sub_category', 'sub_subcategory')
        }),
        
        ("Media", {
                # "description" : "Enter any additional information",
                # "classes": ("collapse",), 
                "fields": ("img",("img_second","img_third"),("img_forth","img_fifth"),"video")
        }),

        ("Added Images", {
                "classes": ("collapse",), 
                "fields": ("first_image",("second_image","third_image"),("forth_image","fifth_image"))
        }),

        ("Feature Points", {
                "fields": (("hightlight_one","hightlight_two"),("hightlight_three","hightlight_four"),("hightlight_five",'hightlight_six'),('hightlight_seven','hightlight_eight'),('hightlight_nine','hightlight_ten'))
        }),

        ("Description", {
                "fields": ("description","specification")
        }),
    )

    def has_delete_permission(self, request, obj = None):
        return False

    @admin.action(description='Mark as Active')
    def make_active(self, request, queryset):
        updated=queryset.update(is_active = True)
        self.message_user(request, ngettext(
            '%d product was successfully marked as published.',
            '%d products were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)


    def store(self, obj):
	    return obj.seller.title  
 
    
    # Category Change
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['buisness_sector'].queryset = Category.objects.filter(parent__isnull=True)
        return super(ProductAdmin, self).render_change_form(request, context, *args, **kwargs)

 

    # Images

    def first_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(url = obj.img.url,width=obj.img.width,height=obj.img.height,))

    def second_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(url = obj.img_second.url,width=obj.img_second.width,height=obj.img_second.height,))
    
    def third_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(url = obj.img_third.url,width=obj.img_third.width,height=obj.img_third.height,))
    
    def forth_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(url = obj.img_forth.url,width=obj.img_forth.width,height=obj.img_forth.height,))

    def fifth_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(url = obj.img_fifth.url,width=obj.img_fifth.width,height=obj.img_fifth.height,))



class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions','indented_title','image']
    search_fields = ['name']
    list_editable=['image']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin) 

