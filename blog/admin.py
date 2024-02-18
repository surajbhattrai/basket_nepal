from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import BlogCategory , Blog

admin.site.register(Blog)


class BlogCategoryAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions','indented_title',]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(BlogCategory, BlogCategoryAdmin) 
