import logging
import random
import time

from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView 

# from basket import version
 
version = 1.0
logger = logging.getLogger('djpwa.pwa.views')


def offline(request):
    return render(request, 'offline.html')

class ServiceWorkerView(TemplateView):
    template_name = 'sw1.js'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["version"] = '1'
        context["manifest"] = static('manifest.json'),
        return context
 
    # def get_context_data(self, **kwargs):
    #     return {
    #         'version': 1,
    #         'icon_url': static('images/logo/logo_icon.png'),
    #         'manifest_url': static('manifest.json'),
    #         'style_url': static('style.css'),
    #         'home_url': reverse('home'),
    #         'offline_url': reverse('offline'),
    #     }


