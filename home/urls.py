from django.urls import path
from .views import PageDetail , ContactView , Home

from django.views.generic import TemplateView

   
urlpatterns = [
    path('',Home.as_view() , name='home'),
    path('page/<slug>/',PageDetail.as_view() , name='pages'),
    path('contact/',ContactView.as_view() , name='contact'),

    path(
        'sw.js',
        TemplateView.as_view(template_name='sw.js', content_type='application/javascript'),
        name='sw.js',
    ),

]