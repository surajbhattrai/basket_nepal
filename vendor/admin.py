from django.contrib import admin
from .models import Seller, Badge ,SocialContact , SellerPages , StoreType ,StoreGallery
from product.models import Category



@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['title','category','mobile','telephone','is_active','created','updated']
    list_display_links =  ['title']
    search_fields = ['title']
    list_per_page = 100
    ordering = ['-created']
    list_editable=['category']
    filter_horizontal = ['badge']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['category'].queryset = Category.objects.filter(parent__isnull=True)
        return super(SellerAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(SocialContact)
class SocialContactAdmin(admin.ModelAdmin):
    list_display = ['seller','facebook','instagram']
    list_display_links =  ['seller']

admin.site.register(Badge)
admin.site.register(SellerPages)



class StoreTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 100
    prepopulated_fields = {'slug': ('name',)}

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['buisness_sector'].queryset = Category.objects.filter(parent__isnull=True)
        return super(StoreTypeAdmin, self).render_change_form(request, context, *args, **kwargs)

admin.site.register(StoreType, StoreTypeAdmin)

admin.site.register(StoreGallery)




    


 