from django.contrib.auth import login,authenticate ,update_session_auth_hash
from django.shortcuts import redirect ,render,get_object_or_404 ,HttpResponseRedirect
from django.urls import reverse_lazy ,reverse 
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, TemplateView , DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.decorators import seller_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import SellerProfileForm , SocialContactForm , SellerPagesForm ,SellerGalleryForm
from accounts.forms import LoginForm, PasswordChangeCustomForm
from address.forms import AddressForm
from accounts.models import User ,SMSActivation
from address.models import Address
from .models import Seller , SocialContact , SellerPages , StoreType , StoreGallery
from product.models import Product , Category
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from address.models import District 
from django.db.models import Q




class Stores(DetailView):
    model = Category
    template_name = "stores.html"

    def get_context_data(self, **kwargs):
        context = super(Stores, self).get_context_data(**kwargs)

        districts = District.objects.all()
        slug= self.kwargs['slug']
        business_sector_obj = get_object_or_404(Category, slug=slug)
        store_types = StoreType.objects.filter(buisness_sector=business_sector_obj)
        stores = Seller.active.filter(category=business_sector_obj).select_related('address__district').order_by('ranking')

        # Search
        query = self.request.GET.get('query')
        search_vectors = (
            SearchVector('title', weight='A'))
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('title', query)
 
        if query:
            stores= stores.annotate(search=search_vectors).filter(Q(search=search_query)).annotate(rank=search_rank + trigram_similarity)

        #location
        location = self.request.GET.get('location')
        if location:
            stores= stores.filter(address__district__district = location)
            districts = districts.exclude(district=location)

        req_store = self.request.GET.get('store')
        if req_store:
            stores= stores.filter(seller_type__slug=req_store)

        paginator = Paginator(stores, 20)            
        page = self.request.GET.get('page')
        try:
            stores = paginator.page(page)
        except PageNotAnInteger:
            stores = paginator.page(1)
        except EmptyPage:
            stores = paginator.page(paginator.num_pages)
        
        context = {
                'business_sector_obj':business_sector_obj,
                'store_types':store_types,
                'stores':stores,
                'districts':districts,
                } 

        return context






class Storefront(DetailView): 
    model = Seller
    template_name = "storefront.html"
        
    def get_context_data(self, **kwargs):
        context = super(Storefront, self).get_context_data(**kwargs)
        slug=self.kwargs.get('slug')

        seller = Seller.objects.get(slug=slug)

        page_obj = SellerPages.objects.filter(seller=seller)
        pages = page_obj.filter(list_as_item=False)
        front_page = page_obj.filter(show_on_frontpage=True)
        deals = page_obj.filter(list_as_item=True)

        gallery = StoreGallery.objects.filter(seller=seller)
        product = Product.objects.filter(seller=seller)

        # Request ---> Query
        query = self.request.GET.get('q')
        search_vectors = (SearchVector('title', weight='A') +SearchVector('description', weight='B'))
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('title', query)

        if query:
            product=product.annotate(search=search_vectors).filter(Q(search=search_query)).annotate(rank=search_rank + trigram_similarity).order_by('-rank')

        paginator = Paginator(product, 40)            
        page = self.request.GET.get('page')
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)

        context = {'product':product,
                   'seller':seller,
                   'pages':pages,
                   'front_page':front_page,
                   'gallery':gallery,
                   'deals':deals,
                } 
        return context    




@method_decorator([seller_required], name='dispatch')
class Dashboard(LoginRequiredMixin,ListView): 
    model = Product
    template_name = "dashboard.html"


    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(seller= self.request.user.seller)[0:8]
        return context

 
class SellerProfile(LoginRequiredMixin, TemplateView):
    seller_form_class = SellerProfileForm
    address_form_class = AddressForm
    template_name = 'seller_profile.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            seller = self.request.user.seller.slug
        except :
            seller = None
        if seller:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        seller_form = self.seller_form_class(request.POST ,request.FILES)
        address_form = self.address_form_class(request.POST ,request.FILES )
        context = self.get_context_data(seller_form=seller_form,address_form=address_form)          
        if address_form.is_valid() and seller_form.is_valid():
            s_obj = seller_form.save(commit=False) 
            s_obj.user = self.request.user
            s_obj.save()
            a_obj = address_form.save(commit=False) 
            a_obj.seller = self.request.user.seller
            a_obj.save()
            return redirect('dashboard')
        return self.render_to_response(context)  

    def form_save(self, form):
        obj = form.save()
        return redirect("dashboard")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



@method_decorator([seller_required], name='dispatch')
class SellerUpdate(LoginRequiredMixin, UpdateView):
    form_class = SellerProfileForm
    model = Seller
    template_name = "dashboard.html" 
 
    def form_valid(self, form):
        super(SellerUpdate, self).form_valid(form)
        messages.success(self.request, 'Your setting is successfully updated!')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('update_seller', kwargs={"slug":self.request.user.seller.slug})
 


@method_decorator([seller_required], name='dispatch')
class SellerAddressUpdate(LoginRequiredMixin,UpdateView):
    form_class = AddressForm
    model = Address
    template_name = "dashboard.html" 
    success_url = reverse_lazy('update_s_address') 

    def form_valid(self, form):
        super(SellerAddressUpdate, self).form_valid(form)
        messages.success(self.request, 'Your address is successfully updated!')
        return redirect(self.success_url)

    def get_object(self):
        return Address.objects.get(seller=self.request.user.seller)



@method_decorator([seller_required], name='dispatch')
class SocialContacts(LoginRequiredMixin, UpdateView): 
    form_class = SocialContactForm
    model = SocialContact
    template_name = "dashboard.html"     
    success_url = reverse_lazy('social') 
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.seller = self.request.user.seller
        return super(SocialContacts, self).form_valid(form)

    def get_object(self, queryset=None):
        obj, created = SocialContact.objects.get_or_create(seller=self.request.user.seller)
        return obj
 

 
@method_decorator([seller_required], name='dispatch')
class SellerPagesList(LoginRequiredMixin, ListView): 
    model = SellerPages
    template_name = "dashboard.html"
    
    def get_queryset(self, *args, **kwargs):
        qs = super(SellerPagesList, self).get_queryset(*args, **kwargs)
        qs = SellerPages.objects.filter(seller=self.request.user.seller).order_by('-created')
        return qs

   
@method_decorator([seller_required], name='dispatch')
class AddNewPage(LoginRequiredMixin, CreateView): 
    form_class = SellerPagesForm
    model = SellerPages
    template_name = "dashboard.html"
    success_url = reverse_lazy('seller_pages')
     
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.seller = self.request.user.seller
        return super(AddNewPage, self).form_valid(form)


 
@method_decorator([seller_required], name='dispatch')
class UpdateSellerPage(LoginRequiredMixin, UpdateView): 
    form_class = SellerPagesForm
    model = SellerPages
    template_name = "dashboard.html"
    success_url = reverse_lazy('seller_pages')
     
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.seller = Seller.objects.get(user=self.request.user)
        return super(UpdateSellerPage, self).form_valid(form)

  
class SellerPagesDetail(DetailView):
    model = SellerPages
    template_name = "seller_page_details.html"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        page = SellerPages.objects.get(slug=slug)
        seller = page.seller
        pages = SellerPages.objects.filter(seller=seller,hide_on_menu=False)
        context = {'page':page,
                   'seller':seller,
                   'pages':pages,
                } 
        return context



@method_decorator([seller_required], name='dispatch')
class SellerGalleryList(LoginRequiredMixin, ListView): 
    model = StoreGallery
    template_name = "dashboard.html"
    
    def get_queryset(self, *args, **kwargs):
        qs = super(SellerGalleryList, self).get_queryset(*args, **kwargs)
        qs = StoreGallery.objects.filter(seller=self.request.user.seller)
        return qs

 
@method_decorator([seller_required], name='dispatch')
class AddGallaryImage(LoginRequiredMixin, CreateView): 
    form_class = SellerGalleryForm
    model = StoreGallery
    template_name = "dashboard.html"
    success_url = reverse_lazy('gallery_list')
    
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.seller = self.request.user.seller
    #     obj.save()
    #     return super(AddGallaryImage, self).form_valid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        current_user = self.request.user.seller
        if current_user.basketnepal_pro :
            obj.seller = current_user
            obj.save()
        else:
            messages.warning(self.request, 'Please upgrade your account to add images.')
        return redirect('gallery_list')



@login_required()
def gallery_image_remove(request, id):
    url = request.META.get('HTTP_REFERER')
    obj = get_object_or_404(StoreGallery, id=id)
    obj.delete()
    messages.warning(request, 'Gallery Image has been deleted!')
    return HttpResponseRedirect(url)
