from django.urls import path
from .views import ServiceWorkerView , offline


urlpatterns = [
    path('sw.js', ServiceWorkerView.as_view(), name='sw.js'),
    path('offline/', offline, name='offline'),
]