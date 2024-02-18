from .models import Pages

def pages(request):
    return {'site_page': Pages.objects.all().order_by('id')}
