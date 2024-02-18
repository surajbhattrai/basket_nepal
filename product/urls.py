from django.urls import path
from .views import ProductDetail , load_subcategory , product_remove , AddProduct, AllProducts, ProductUpdate , ProductListView
urlpatterns = [
    path('product/<slug>',ProductDetail.as_view() , name='product_detail'),
    path('ajax/ajax_sub_cat/', load_subcategory, name='ajax_sub_cat'),
    path('product/remove/<slug>',product_remove, name='product_remove'),

    #dashboard
    path('dashboard/addproduct/',AddProduct.as_view() , name='addproduct'),
    path("dashboard/update/<slug>/",ProductUpdate.as_view(), name="updateproduct"),
    path('dashboard/allproducts/',AllProducts.as_view() , name='allproducts'),

    path('products/',ProductListView.as_view() , name='products_listview'),
    
]      