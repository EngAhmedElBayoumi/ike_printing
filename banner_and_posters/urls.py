#import path , viwes
from django.urls import path

from . import views

app_name = "banner_and_posters"

urlpatterns = [
    path("",views.banner_and_posters,name="banner_and_posters"),
]



