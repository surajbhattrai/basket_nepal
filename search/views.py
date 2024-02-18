from django.shortcuts import render , redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from django.db.models import Q, F, Count, Subquery, Prefetch
from itertools import chain
from .models import SearchTerms
from address.models import District 
from product.models import Product ,Category
from vendor.models import  Seller   
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
 

 
class SearchView(ListView):
    template_name = 'search.html'
    count = 0
    queryset = Product.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['count'] = context.get('object_list').count()
        query = self.request.GET.get('q')
        show = self.request.GET.get('show')
        cat = self.request.GET.get('list')
        location = self.request.GET.get('location')

        search_vectors = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='B')
            )

        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('title', query)

        if query:
            self.update_search_query(query)  

            products= Product.objects.annotate(search=search_vectors).filter(Q(search=search_query,is_active=True,seller__is_active=True)).annotate(rank=search_rank + trigram_similarity).order_by('seller__ranking','-rank')

            categories = Category.objects.filter(product_subsubcatgeory__in=products).distinct()[0:20]
 
            if location:
                products = products.filter(Q(seller__user__address__district__district=location)).order_by('seller__rank')


            if cat:
                products= products.filter(Q(sub_subcategory__slug=cat))
            
        paginator = Paginator(products, 40)            
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        district = District.objects.all()

        if location:
            district = district.exclude(district=location)
    
        context = {
            'products': products,
            'categories':categories,
            'district':district,
        }

        if location:
            context['area'] = Area.objects.filter(district__district=location)

        return context

    def update_search_query(self, query):
        term, _ = SearchTerms.objects.get_or_create(
            defaults={'search_terms':query}, 
            search_terms__iexact=query
        )
        term.total_searches += 1
        term.save()        


    # def get_queryset(self, *args, **kwargs):
    #     query = self.request.GET['q']
    #     if not query:
    #         return redirect('home')
        #    self.update_search_query(query)
        #    return Product.objects.filter(Q(title__icontains=query))
        # return super().get_queryset()

           
    





     

