from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from requests.models import codes
from accounts.models import User ,SMSActivation
import django.apps
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm 
from buyers_requests.models import Request


@admin.register(User)
class AccountAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    list_display = ('full_name','phone','seller')
    list_display_links =  ('full_name', 'phone')
    ordering = ('-date_joined',)
    filter_horizontal = 'groups','user_permissions'
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'fields': ('phone','password1', 'password2'),
        }),
    )

    def full_name(self, obj):
	    return obj.get_full_name()

    # Post your requests

    # def request_counts(self, obj):
    #     item = Request.objects.filter(user=obj).count()
    #     return item
    # request_counts.short_description = "No of Requests"

    # def view_requests(self, obj):
    #     link = (
    #         reverse("admin:salesinfo_vehicletype_changelist")  + "?" + urlencode({"id": obj.vehicletype.id})
    #     )
    #     return format_html('<b><a href="{}">{}</a></b>', link, obj.vehicletype)
    # view_requests.short_description = "View All Requests"
 


@admin.register(SMSActivation)
class SMSActivationAdmin(admin.ModelAdmin):
    date_hierarchy = 'update'
    list_display = ('full_name','phone' ,'code','resend','activated')
    list_display_links =  ('full_name','phone' ,'code','activated')
    search_fields = ['phone']
    list_filter = ['activated']

    def full_name(self,obj):
        return obj.user.get_full_name()



@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_filter = ['user','content_type','action_flag']
    search_fields = ['object_repr','change_message',]
    list_display = ['action_time','user','content_type','object_link','action_flag',]

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"









