from django.db import models
from accounts.models import User
from product.models import Product
from buyers_requests.models import Request
from django.urls import reverse


class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="convo_starter")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="convo_participant")
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk":self.pk})

  
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="message_receiver")

    product = models.ForeignKey(Product, null=True ,blank=True , on_delete=models.SET_NULL)
    request = models.ForeignKey(Request, null=True ,blank=True , on_delete=models.SET_NULL)

    text = models.CharField(max_length=200)
    attachment = models.ImageField(blank=True, upload_to="inbox/")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    seen = models.BooleanField(default=False)



 