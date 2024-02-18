from inbox.models import Message
from django.db.models import Q, Max
from django.db.models.functions import Coalesce

def unseen(request):
    try:
        qs = Message.objects.filter(receiver=request.user, seen=False)
        return {'unread_message': qs}
    except:
        return {'unread_message': []}




    
