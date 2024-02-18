from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

#models
from product.models import Product
from buyers_requests.models import Request
from vendor.models import Seller , SellerPages
from home.models import Pages


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['home','request']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Product.active.all()

    def lastmod(self, obj):
        return obj.published


class RequestSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Request.objects.filter(approved=True)

    def lastmod(self, obj):
        return obj.created


class StoresSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Seller.active.all()

    def lastmod(self, obj):
        return obj.created


class SellePageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return SellerPages.objects.all()

    def lastmod(self, obj):
        return obj.created


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Pages.object.all()

    def lastmod(self, obj):
        return obj.created