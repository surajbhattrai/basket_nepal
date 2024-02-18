from django import forms
from .models import Contact
from django.forms import Textarea,TextInput, Select, FileInput, NumberInput,ModelForm,EmailInput

 
class ContactForm(ModelForm):

    class Meta():
        model = Contact
        fields = ('first_name', 'last_name','email','phone','message')
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'phone': TextInput(attrs={'class': 'form-control','placeholder': '+977'}),
            'email': EmailInput(attrs={'class': 'form-control','placeholder': 'hello@gmail.com'}),
            'message': Textarea(attrs={'class':"form-control",'placeholder': "Message", 'rows':'4'}),
        }
