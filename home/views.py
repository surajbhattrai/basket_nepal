from django.views.generic import ListView, DetailView, CreateView
from .models import Pages , Contact ,Sliders
from .forms import ContactForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from vendor.models import  Seller 
from product.models import Category , Product
from django.db.models import Q

  
class Home(ListView):
    template_name = "home.html"
    model = Seller

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        products = Product.active.all().order_by('-published')[0:20]
        sliders = Sliders.objects.all().order_by('-id')
        context = {'products':products,'sliders':sliders} 
        return context

    

class PageDetail(DetailView):
    model = Pages
    template_name = "page.html"


class ContactView(SuccessMessageMixin,CreateView):
    model = Contact
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    success_message = 'Sent Successfull. We will contact you soon.'





 