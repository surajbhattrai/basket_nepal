from django import forms
from .models import Message
from django.forms import ModelForm, TextInput, Textarea, Select, FileInput , NumberInput , RadioSelect

class SendMessageForm(ModelForm):

    class Meta():
        model = Message
        fields = ('receiver', 'text','attachment')

