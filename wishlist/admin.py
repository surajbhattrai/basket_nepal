from django.contrib import admin
from .models import Wishlist ,WishlistItem

admin.site.register(Wishlist)

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['wishlist','product','created']
    search_fields = ['name']
    list_filter = ['created']
    list_per_page = 100
    search_fields = ['wishlist','product']

