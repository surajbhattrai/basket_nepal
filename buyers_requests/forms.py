from django import forms
from .models import Request
from product.models import Category 
from vendor.models import StoreType
from django.forms import Textarea,TextInput, Select, FileInput, NumberInput,ModelForm,CheckboxSelectMultiple, ModelMultipleChoiceField, RadioSelect ,CheckboxInput

from crispy_forms.helper import FormHelper

    
class RequestForm(ModelForm):

    # store_type = forms.ModelMultipleChoiceField(
    #     queryset=StoreType.objects.all(),
    #     widget=CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
    #     )

    class Meta():
        model = Request
        fields = ('price', 'content','quantity','image','product_name','purpose' ,'business_sector','district','show_contact_info')
        widgets = {
            'price': TextInput(
                attrs={'class': 'form-control text-left', "data-inputmask-alias":"numeric" ,'placeholder': ' Rs.'}),
            'quantity': NumberInput(attrs={'class': 'form-control', 'placeholder': '10 Pieces / 10 Kg'}),
            'content': Textarea(attrs={'class':"form-control",'placeholder': "Describe what are you looking for ?", 'rows':'4'}),
            'product_name': TextInput(attrs={'class':"form-control",'placeholder': "Name of product your are looking for."}),
            # 'store_type': Select(attrs={'class': 'form-control','placeholder': 'Category'}),
            'purpose': RadioSelect(attrs={'class': 'list-unstyled list-inline'}),
            'image': FileInput(attrs={'class': 'mb-3' }),  

            'business_sector' : Select(attrs={'class': 'form-control','placeholder': 'Category'}), 
            'district' : Select(attrs={'class': 'form-select'}),
            'show_contact_info' : CheckboxInput(attrs={'class': 'form-check-input '}),
              
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['business_sector'].queryset = Category.objects.filter(parent=None)



