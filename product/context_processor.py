from .models import Category

def sectors(request):
    return {'all_sectors': Category.objects.filter(parent=None)}
