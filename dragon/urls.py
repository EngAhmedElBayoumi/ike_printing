#import path , views

from django.urls import path

from . import views

app_name = "dragon"

urlpatterns = [
    path("",views.get_available_time,name="get_available_time"),
]

