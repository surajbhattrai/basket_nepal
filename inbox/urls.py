from django.urls import path
from .views import Conversations , ConversationDetail , send_message, send_product_message ,send_request_message

urlpatterns = [
    path("send_message/<int:id>/", send_message, name="send_message"),
    path("send_product_message/<str:slug>/", send_product_message, name="send_product_message"),
    path("send_request_message/<int:id>/", send_request_message, name="send_request_message"),

    path("chat/<int:pk>/", ConversationDetail.as_view(), name="message_detail"),
    path("chat/", Conversations.as_view(), name="message_list"),
]
 