from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView 

# import debug_toolbar

from django.contrib.sitemaps.views import sitemap

from django.contrib.sitemaps import views
from django.views.decorators.cache import cache_page

from .sitemaps import StaticSitemap, ProductSitemap , RequestSitemap ,StoresSitemap , SellePageSitemap

sitemaps = {
    'static': StaticSitemap,
    'product': ProductSitemap,
    'request': RequestSitemap,
    'store' : StoresSitemap,
    'sellerpage':SellePageSitemap,

}

 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('product.urls')),
    path('',include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')), 
    path('',include('buyers_requests.urls')),
    path('',include('wishlist.urls')),
    # path('',include('search.urls')),
    path('',include('address.urls')),
    path('',include('vendor.urls')),
    path('',include('home.urls')),
    path('',include('blog.urls')),
    path('',include('inbox.urls')),
    path('',include('pwa.urls')),

    # path('__debug__/', include('debug_toolbar.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')), 


    
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")), 

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'), 
    path('sitemap-<section>.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name='sitemaps'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_title = "Basket Nepal"
admin.site.index_title = "Basket Nepal"
admin.site.site_header = "Basket Nepal"



