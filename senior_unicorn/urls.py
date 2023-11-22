#import path , views

from django.urls import path

from . import views

app_name = "senior_unicorn"

urlpatterns = [
    path("",views.senior_unicorn,name="senior_unicorn"),
]

