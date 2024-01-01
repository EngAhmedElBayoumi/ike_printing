#import path , views

from django.urls import path

from . import views

app_name = "call_expert"

urlpatterns = [
    path("",views.call_expert,name="call_expert"),
    path("call_senior_designer/",views.call_senior_designer,name="call_senior_designer"),
    path("callEpertTwo/",views.call_designer,name="callEpertTwo"),
    path("payment/success/",views.payment_success,name="payment_success"),
    path("payment/failed/",views.payment_failed,name="payment_failed"),
    path("redirect_to_payment/",views.redirect_to_payment,name="redirect_to_payment"),
]
