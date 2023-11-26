#import path , views

from django.urls import path

from . import views

app_name = "call_expert"

urlpatterns = [
    path("",views.call_expert,name="call_expert"),
    path("call_senior_designer/",views.call_senior_designer,name="call_senior_designer"),
    path("callEpertTwo/",views.call_designer,name="callEpertTwo"),
    path("payment/success/",views.call_designer,name="payment-success"),
    path("payment/failed/",views.call_designer,name="payment-failed"),
    
]
