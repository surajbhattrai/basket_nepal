from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, reverse, render
from accounts.models import User
from .models import Conversation , Message

from product.models import Product
from buyers_requests.models import Request

from .forms import SendMessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView
from django.shortcuts import render, redirect, 	get_object_or_404,HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.db.models import Prefetch, Count

  


class Conversations(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = "inbox.html"

    def get_context_data(self, **kwargs):
        context = super(Conversations, self).get_context_data(**kwargs)
        qs = Conversation.objects.filter(Q(user1=self.request.user) | Q(user2=self.request.user)).annotate(last_message_sent=Coalesce(Max("message__timestamp"), "timestamp")).select_related('user1','user2').order_by("-last_message_sent")
        paginator = Paginator(qs,8) 
        page = self.request.GET.get('page')
        conversations = paginator.get_page(page)
        context['conversations'] = conversations
        return context

   
class ConversationDetail(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = "inbox.html"


    def get_context_data(self, **kwargs):
        context = super(ConversationDetail, self).get_context_data(**kwargs)
        conversations = self.get_conv()
        context['conversations'] = conversations
        context['page_obj'] = conversations

        msg = Message.objects.filter(conversation__id=self.kwargs.get('pk')).select_related("sender__seller",'receiver__seller','product','conversation')
        msg.filter(seen=False).exclude(sender=self.request.user).update(seen=True)
        context['msg'] = Message.objects.filter(conversation__id=self.kwargs.get('pk')).select_related("sender__seller",'receiver__seller','product','conversation')
        return context
 

    def get_conv(self):
        queryset = Conversation.objects.filter(Q(user1=self.request.user) | Q(user2=self.request.user)).annotate(last_message_sent=Coalesce(Max("message__timestamp"), "timestamp")).select_related('user1','user2').order_by("-last_message_sent")
        
        paginator = Paginator(queryset,8) 
        page = self.request.GET.get('page')
        conversations = paginator.get_page(page)
        return conversations





 

@login_required()
def send_message(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST' or request.FILES['attachment']:
        conversation = get_object_or_404(Conversation, id=id)
        receiver = User.objects.get(id=request.POST.get('receiver'))
        text = request.POST.get('text')
        attachment = request.FILES.get('attachment')
        message = Message(sender=request.user, text=text, conversation=conversation,attachment=attachment, receiver=receiver)
        message.save()
    return HttpResponseRedirect(url)


@login_required()
def send_product_message(request, slug):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        product = get_object_or_404(Product, slug=slug)
        receiver = product.seller.user
        text = request.POST.get('text')

        try:
            qs = Conversation.objects.get(Q(user1=request.user , user2=receiver) | Q(user1=receiver, user2=request.user))
        except Conversation.DoesNotExist :
            qs , qsCreated = Conversation.objects.get_or_create(user1=request.user,user2=receiver)

        message = Message(sender=request.user, text=text, conversation=qs, receiver=receiver, product=product)
        message.save()

        messages.success(request, 'Message send successfull !')
    return HttpResponseRedirect(url)


 
@login_required()
def send_request_message(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        request_obj = get_object_or_404(Request, id=id)
        text = request.POST.get('text')

        try:
            qs = Conversation.objects.get(Q(user1=request_obj.user , user2=request.user) | Q(user1=request.user, user2=request_obj.user))
        except Conversation.DoesNotExist :
            qs , qsCreated = Conversation.objects.get_or_create(user1=request_obj.user,user2=request.user)

        message = Message(sender=request.user, text=text, conversation=qs, receiver=request_obj.user, request=request_obj)
        message.save()

        messages.success(request, 'Message send successfull !')
    return HttpResponseRedirect(url)