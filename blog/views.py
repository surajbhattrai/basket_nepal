from django.shortcuts import render, get_object_or_404
from .models import BlogCategory , Blog
from django.views.generic import ListView, DetailView

class BlogList(ListView):
    model = Blog
    template_name = "blog.html"
    paginate_by = 20

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["blog_category"] = BlogCategory.objects.all()
        return context 


class BlogDetail(DetailView):
    model = Blog
    template_name = "blog_single.html"
    context_object_name = "blog"


class BlogCategoryView(ListView): 
    model = Blog
    template_name = "blog.html"
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super(BlogCategoryView, self).get_queryset(*args, **kwargs)
        slug= self.kwargs['slug']
        category=get_object_or_404(BlogCategory,slug=slug)
        qs = Blog.objects.filter(category=category).order_by('-published')
        return qs

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["blog_category"] = BlogCategory.objects.all()
        return context
