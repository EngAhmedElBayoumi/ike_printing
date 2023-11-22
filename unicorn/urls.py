#import path , views

from django.urls import path

from . import views

app_name = "unicorn"

urlpatterns = [
    path("",views.unicorn,name="unicorn"),
]

