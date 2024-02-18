from django.urls import path
from .views import BlogList, BlogCategoryView , BlogDetail
   
urlpatterns = [
    path('blog/',BlogList.as_view() , name='blog_list'),
    path('blog_category/<slug>/',BlogCategoryView.as_view() , name='blog_category'),
    path('blog/<slug>',BlogDetail.as_view() , name='blog_detail'),
]