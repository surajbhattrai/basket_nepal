from django import forms
from vendor.models import Seller 
from .models import SocialContact , SellerPages , StoreGallery
from django.forms import TextInput, FileInput ,NumberInput ,Textarea ,EmailInput ,CheckboxInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.contrib import messages
 

class SellerProfileForm(forms.ModelForm):

    class Meta:
        model = Seller
        fields = ['title','bio','position','logo','registration_no','business_document','banner','mobile','business_email','telephone'] 
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control form-control-sm'}),
            'position': TextInput(
                attrs={'class': 'form-control form-control-sm'}),
            'mobile': TextInput(
                attrs={'class': 'form-control form-control-sm'}),
            'telephone': TextInput(
                attrs={'class': 'form-control form-control-sm'}),
            'business_email': EmailInput(
                attrs={'class': 'form-control form-control-sm'}),
            'logo': FileInput(
                attrs={'class': 'form-control py-2'}),
            'banner': FileInput( attrs={'class': 'form-control py-2'}),
            'registration_no': NumberInput( attrs={'class': 'form-control form-control-sm'}),
            'business_document': FileInput( attrs={'class': 'form-control'}),
            'bio': Textarea(attrs={'class':'form-control','rows':'4'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class SocialContactForm(forms.ModelForm):

    class Meta:
        model = SocialContact
        fields = ['facebook','instagram'] 
        widgets = {
            'facebook': TextInput(
                attrs={'class': 'form-control form-control-sm'}),
            'instagram': TextInput(
                attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False



class SellerPagesForm(forms.ModelForm):

    class Meta:
        model = SellerPages
        fields = ['image','title','content','list_as_item','show_on_frontpage']
        widgets = {
            'image': FileInput(attrs={'class': 'form-control py-2'}),
            'title': TextInput(
                attrs={'class': 'form-control'}),
            'list_as_item' : CheckboxInput({'class': 'form-check'}),
            'show_on_frontpage' : CheckboxInput({'class': 'form-check'}),
            'content': Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class SellerGalleryForm(forms.ModelForm):
    class Meta:
        model = StoreGallery
        fields = ['image'] 
        widgets = {
            'image': FileInput(attrs={'class': 'form-control py-2'}),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    # def clean(self):
    #     cleaned_data = super().clean()
    #     if not self.instance.seller.basketnepal_pro:
    #         # messages.warning(self.request, 'Please Upgrade your account to add images.')
    #         raise forms.ValidationError("Please upgrade your account to add images.")
    #     return cleaned_data

 