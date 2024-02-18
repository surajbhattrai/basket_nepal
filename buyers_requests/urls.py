from django.urls import path
from .views import request_delete ,SubmitRequest,hide_request,RequestList 

urlpatterns = [
    path('request', SubmitRequest.as_view(), name="request"),
    path("request/<id>/remove", request_delete , name="remove_request"),
    path('requests/',RequestList.as_view(), name="request_list"),
    path('hide_request/<int:id>/', hide_request, name='hide_request'),
]     