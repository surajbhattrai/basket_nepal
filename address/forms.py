from django import forms
from .models import Address, District
from django.forms import Select ,TextInput


 
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['building','city','district','province']
        widgets = {
            'building' :TextInput(attrs={'class': 'form-control form-control-sm','placeholder': 'Example : 2nd Floor , Computer Bazar.'}),
            'city' :TextInput(attrs={'class': 'form-control form-control-sm','placeholder': 'Example : Putalisadak'}),
            'district': Select(attrs={'class': 'form-control form-control-sm'}),
            'province' :Select(attrs={'class': 'form-control form-control-sm'}),
        }
 
    # def __init__(self, *args, **kwargs):
    #     super(AddressForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control form-control-sm'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['district'].queryset = District.objects.none()

    #     if 'province' in self.data:
    #         try:
    #             province_id = int(self.data.get('province'))
    #             self.fields['district'].queryset = District.objects.get(id=province_id)
    #         except (ValueError, TypeError):
    #             pass
    

  