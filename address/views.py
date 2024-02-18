from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.contrib import messages
from .models import Address, District, Province
from .forms import AddressForm
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

 
def add_address(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = Address()
            data.building =  form.cleaned_data['building']
            data.city =  form.cleaned_data['city']
            data.district =  form.cleaned_data['district']
            data.province =  form.cleaned_data['province']
            data.seller = request.user.seller
            data.save()
            messages.success(request, 'New address has been successfully added!')
            return HttpResponseRedirect(url)
        else:
             form = AddressForm()
    return HttpResponseRedirect(url)

 
def load_districts(request):
    province_id = request.GET.get('province')
    province=get_object_or_404(Province,id=province_id)
    district = District.objects.filter(province=province)
    return render(request, 'ajax_district.html', {'district': district})



