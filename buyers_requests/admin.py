from django.contrib import admin
from .models import Request ,HideRequest

 
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['content','image','customer_budget','customer','quantity','approved']
    list_display_links =  ['content','customer']
    search_fields = ['content']
    list_per_page = 100
    list_filter = ['created',]
    ordering = ['-created']
    list_editable=['approved']

    def phone(self, obj):
	    return obj.user.phone
    
    def customer(self,obj):
        return obj.user.get_full_name()

    def customer_budget(self,obj):
        return 'Rs. '+str(obj.price)
    
admin.site.register(HideRequest) 


