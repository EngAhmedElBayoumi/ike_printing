#import path , views

from django.urls import path

from . import views

app_name = "senior_dragon"

urlpatterns = [
    path("",views.senior_dragon,name="senior_dragon"),
]

