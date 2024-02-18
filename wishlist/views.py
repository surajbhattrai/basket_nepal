from django.shortcuts import render, redirect, 	get_object_or_404,HttpResponseRedirect
from .models import Wishlist , WishlistItem
from vendor.models import Seller
from product.models import Product
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

 

@login_required()
def wishlist_add(request, id):
    obj, created = Wishlist.objects.update_or_create(user=request.user)
    product = get_object_or_404(Product, id=id)
    item, itemCreated = WishlistItem.objects.update_or_create(wishlist=obj, product=product)
    obj.wishlist_items.add(item)
    item.save()
    obj.save()
    messages.success(request, 'Product saved for later!')
    return redirect("product_detail", slug=product.slug)
 
 
@login_required()
def wishlist_remove(request, slug):
    url = request.META.get('HTTP_REFERER')
    obj, created = Wishlist.objects.update_or_create(user=request.user)
    product = get_object_or_404(Product, slug=slug)
    wishlistItems = WishlistItem.objects.filter(wishlist=obj, product=product)
    wishlistItems.delete()
    messages.warning(request, 'Product has been removed!')
    return HttpResponseRedirect(url)

 
class MyWishlist(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "mywishlist.html"
    context_object_name = 'saved'
    paginate_by=20

 
    def get_queryset(self, *args, **kwargs):
        qs = super(MyWishlist, self).get_queryset(*args, **kwargs)
        wishlist, created = Wishlist.objects.get_or_create(user= self.request.user)
        qs = qs.select_related('product').filter(wishlist=wishlist).order_by('-created')
        return qs 