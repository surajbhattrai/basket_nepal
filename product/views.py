from django.shortcuts import render, HttpResponseRedirect ,get_object_or_404 ,redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q ,Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.urls import reverse_lazy
from .forms import ProductForm 
from .models import Product , Category
from address.models import District 
from vendor.models import Seller , StoreType
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
from accounts.decorators import seller_required
from wishlist.models import WishlistItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 



  
class ProductDetail(DetailView):
    model = Product
    template_name = "product.html"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        product=Product.objects.select_related('seller').get(slug=slug)
        context["related_product"] = Product.objects.filter(sub_subcategory=product.sub_subcategory).exclude(id=product.id)[0:6]
        if self.request.user.is_authenticated: 
            context["saved"] = WishlistItem.objects.select_related('wishlist').filter(wishlist__user=self.request.user ,product=product)
        return context


@method_decorator([seller_required], name='dispatch')
class AddProduct(LoginRequiredMixin, CreateView): 
    form_class = ProductForm
    model = Product
    template_name = "addproduct.html"
    success_url = reverse_lazy('allproducts')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs
     
    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.seller = self.request.user.seller
    #     return super(AddProduct, self).form_valid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        current_user = self.request.user.seller
        if current_user.basketnepal_pro :
            obj.seller = current_user
            obj.save()
        else:
            messages.warning(self.request, 'Please upgrade your account to add products.')
        return redirect('allproducts')

 
@method_decorator([seller_required], name='dispatch')
class ProductUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProductForm
    model = Product
    template_name = "updateproduct.html" 
    success_url = reverse_lazy('allproducts')
     
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.seller = Seller.objects.get(user=self.request.user)
        return super(ProductUpdate, self).form_valid(form)



 
@method_decorator([seller_required], name='dispatch')
class AllProducts(LoginRequiredMixin, ListView):
    model = Product
    template_name = "allproducts.html"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super(AllProducts, self).get_queryset(*args, **kwargs)
        search = self.request.GET.get('search',None)
        qs = Product.objects.filter(seller=self.request.user.seller).order_by('-published')
        if search:
            qs = qs.annotate(search=(SearchVector('title'))).filter(Q(search=search))
        return qs


 

class ProductListView(ListView):
    model = Category
    template_name = "business.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        districts = District.objects.all()        
        category = Category.objects.filter(level=1)
        products = Product.active.all().order_by('seller__ranking')
        
        # Search
        query = self.request.GET.get('q')
        search_vectors = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='B')
            )
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('title', query)

        if query:
            products= products.annotate(search=search_vectors).filter(Q(search=search_query)).annotate(rank=search_rank + trigram_similarity)
 
        # GET request ---> Catgeory
        request_category = self.request.GET.get('category', None)
        sub_category = []
        if request_category:
            sub_category= Category.objects.get(slug=request_category).get_children()
            products = products.filter(category__slug=request_category)

        # GET request ---> Sub Catgeory
        request_sub_category = self.request.GET.get('subcategory', None)
        sub_subcategory = []
        if request_sub_category:
            sub_subcategory= Category.objects.get(slug=request_sub_category).get_children()
            products = products.filter(sub_category__slug=request_sub_category)

        # GET request ---> Sub_Subcatgeory
        request_sub_subcategory = self.request.GET.get('sub_subcategory', None)
        if request_sub_subcategory:
            products = products.filter(sub_subcategory__slug=request_sub_subcategory)

        #location
        location = self.request.GET.get('location')
        if location:
            products= products.filter(seller__address__district__district = location)
            districts = districts.exclude(district=location)

        #price low
        price = self.request.GET.get('price')
        if price:
            products= products.order_by('price')

        paginator = Paginator(products, 60)            
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
                'category':category,
                'sub_category':sub_category,
                'sub_subcategory':sub_subcategory,
                'products': products,
                'districts':districts,
                } 

        return context  
 




# ajax
 
def load_subcategory(request):
    category_id = request.GET.get('category')
    category=get_object_or_404(Category,id=category_id)
    sub_category = category.get_children()
    return render(request, 'sub_cat.html', {'sub_category': sub_category})



@login_required()
def product_remove(request, slug):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    messages.warning(request, 'Product has been deleted!')
    return HttpResponseRedirect(url)

 


 





