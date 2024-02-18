from django.urls import path
from .views import SellerProfile, SellerUpdate , SellerAddressUpdate, SocialContacts ,  SellerPagesList, Dashboard , Storefront , AddNewPage , UpdateSellerPage, SellerPagesDetail , Stores , SellerGalleryList, AddGallaryImage , gallery_image_remove

 
urlpatterns = [ 
    path('seller-profile/',SellerProfile.as_view(),name='seller_profile'),
    path("dashboard/settings/<str:slug>/",SellerUpdate.as_view(), name="update_seller"),

    path('dashboard/',Dashboard.as_view() ,name='dashboard'),
    
    #settings
    path("dashboard/address/update/",SellerAddressUpdate.as_view(), name="update_s_address"),
    path("dashboard/social/",SocialContacts.as_view(), name="social"),

    #pages
    path("dashboard/pages/",SellerPagesList.as_view(), name="seller_pages"),
    path("dashboard/add-page/",AddNewPage.as_view(), name="add_new_pages"),
    path("dashboard/update-page/<int:pk>",UpdateSellerPage.as_view(), name="update_page"),

    #gallery
    path("dashboard/gallery/",SellerGalleryList.as_view(), name="gallery_list"),
    path("dashboard/add-image/",AddGallaryImage.as_view(), name="add_gallery_image"),
    path("dashboard/remove-gallery-image/<int:id>", gallery_image_remove , name="remove_gallery_image"),

    path('<str:slug>/storefront/', Storefront.as_view() , name='storefront'),
    path('seller-page/<str:slug>/', SellerPagesDetail.as_view() , name='seller_page_detail'),
    
    path('stores/<str:slug>',Stores.as_view() , name='stores'),
]

  