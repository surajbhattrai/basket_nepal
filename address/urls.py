from django.urls import path
from .views import add_address ,load_districts

urlpatterns = [
    path('add_address/',add_address,name='add_address'),
    path('ajax/load_districts/', load_districts, name='ajax_load_districts'),
]
