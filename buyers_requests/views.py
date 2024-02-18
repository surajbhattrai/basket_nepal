from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from product.models import Product, Category
from accounts.models import User
from vendor.models import  Seller  
from address.models import District
from inbox.models import Message
from .forms import RequestForm 
from .models import Request , HideRequest
from address.models import Address
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from accounts.decorators import seller_required

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q ,Count
from django.core.paginator import Paginator



class SubmitRequest(LoginRequiredMixin ,CreateView):
    form_class = RequestForm
    model = Request
    template_name = "submit_request.html"
    success_url = reverse_lazy('request_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        messages.success(self.request, 'Your request is successfully sent!')
        return super(SubmitRequest, self).form_valid(form)

 

@login_required()
def request_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    buyers_request = Request.objects.filter(id=id, user_id=current_user.id)
    buyers_request.delete()
    messages.warning(request, 'Your Request has been deleted.')
    return HttpResponseRedirect(url)
 

@login_required()
@seller_required
def hide_request(request, id):
    url = request.META.get('HTTP_REFERER')
    current_seller= request.user.seller
    request = Request.objects.get(id=id)
    obj, created = HideRequest.objects.update_or_create(seller=current_seller, request=request)
    obj.save()
    return HttpResponseRedirect(url)


class RequestList(ListView):
    model = Request
    template_name = "seller_request.html"
    context_object_name = "requests"

    def get_queryset(self, *args, **kwargs):
        qs = super(RequestList, self).get_queryset(*args, **kwargs)

        if self.request.user.is_authenticated:
            messages = Message.objects.filter(sender=self.request.user,request__isnull=False)
            qs = Request.objects.filter(approved=True).exclude(id__in = [i.request.id for i in messages]).exclude(user=self.request.user).select_related('district').order_by('-created')
        else:
            qs = Request.objects.filter(approved=True).select_related('district').order_by('-created')

            # , created__gte=datetime.now()-timedelta(days=7)

        #Location
        location = self.request.GET.get('location')
        if location:
            qs= qs.filter(district__district = location)

        #Search
        query = self.request.GET.get('search')
        search_vectors = (
            SearchVector('product_name', weight='A') +
            SearchVector('content', weight='B')
            )
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('product_name', query)
        if query:
            qs= qs.annotate(search=search_vectors).filter(Q(search=search_query)).annotate(rank=search_rank + trigram_similarity)


        yours = self.request.GET.get('view')
        if yours:
            qs = Request.objects.filter(user=self.request.user)

        # qs = random.sample(list(qs), len(qs))[0:100]
        return qs
        
    def get_context_data(self, **kwargs): 
        context = super(RequestList, self).get_context_data(**kwargs)
        # context['request'] = random.sample(list(request), len(request))[0:100]
        context['districts'] = District.objects.all()
        return context


# request = BuyersRequest.objects.filter(category__in=category, user__userprofile__district=self.request.user.seller.district, created__gte=datetime.now()-timedelta(days=7)).exclude(proposal__in=proposal)



     

   


        


        

