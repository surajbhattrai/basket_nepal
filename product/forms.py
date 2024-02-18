from django import forms
from .models import Product, Category 
from django.forms import ModelForm, TextInput, Textarea, Select, FileInput , NumberInput , RadioSelect
from crispy_forms.helper import FormHelper
from django.contrib import messages

 
 
class ProductForm(ModelForm):

    class Meta():
        model = Product
        fields = (
                'title','description','specification','brand','price',
                'buisness_sector','category','sub_category','sub_subcategory',
                'img', 'img_second', 'img_third', 'img_forth','img_fifth','video',
                'hightlight_one','hightlight_two','hightlight_three','hightlight_four','hightlight_five','hightlight_six','hightlight_seven','hightlight_eight','hightlight_nine','hightlight_ten'
                ) 
                
        widgets = {

            'title': TextInput(
                attrs={'class': 'form-control ','placeholder': 'Product Title '}),
            'brand': TextInput(
                attrs={'class': 'form-control ','placeholder': 'Brand Name'}),
            'price': NumberInput(
                attrs={'class': 'form-control ', 'placeholder': ' Rs. '}),

            'buisness_sector': Select(attrs={'class': ' '}), 
            'category': Select(attrs={'class': ' '}), 
            'sub_category': Select(attrs={'class': '  '}), 
            'sub_subcategory': Select(attrs={'class': '  '}), 

            'description': Textarea(),
            'specification': Textarea(),
                       
            'hightlight_one': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 1'}),
            'hightlight_two': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 2'}),
            'hightlight_three': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 3'}),
            'hightlight_four': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 4'}),
            'hightlight_five': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 5'}),
            'hightlight_six': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 6'}),
            'hightlight_seven': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 7'}),
            'hightlight_eight': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 8'}),
            'hightlight_nine': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 9'}),
            'hightlight_ten': TextInput(
                attrs={'class': 'form-control my-2','placeholder': 'Feature point 10'}),
            
            'img': FileInput(attrs={'class': 'form-control'}),
            'img_second': FileInput(attrs={'class': 'form-control'}),
            'img_third': FileInput(attrs={'class': 'form-control'}),
            'img_forth': FileInput(attrs={'class': 'form-control'}),
            'img_fifth': FileInput(attrs={'class': 'form-control'}),

            'video': TextInput(
                attrs={'class': 'form-control  ','placeholder': 'Enter product video URL'}),

        }

 
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.fields['buisness_sector'].queryset = Category.objects.filter(parent=None)
        self.fields['category'].queryset = Category.objects.none()
        self.fields['sub_category'].queryset = Category.objects.none()
        self.fields['sub_subcategory'].queryset = Category.objects.none()

        if 'category' in self.data:
            try:
                buisness_sector_id = int(self.data.get('buisness_sector'))
                category_id = int(self.data.get('category'))
                sub_category_id = int(self.data.get('sub_category'))
                self.fields['category'].queryset = Category.objects.get(id=buisness_sector_id).get_children()
                self.fields['sub_category'].queryset = Category.objects.get(id=category_id).get_children()
                self.fields['sub_subcategory'].queryset = Category.objects.get(id=sub_category_id).get_children()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            sec = self.instance.buisness_sector
            cat = self.instance.category
            sub_cat = self.instance.sub_category 
            self.fields['category'].queryset = sec.get_children()
            self.fields['sub_category'].queryset = cat.get_children()
            self.fields['sub_subcategory'].queryset = sub_cat.get_children()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if not self.request.user.seller.basketnepal_pro:
    #         messages.warning(self.request, 'Please Upgrade your account to add images.')
    #         raise forms.ValidationError("Please upgrade your account to add products.")
    #     return cleaned_data
 











