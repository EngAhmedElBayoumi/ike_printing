#import path , views

from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("",views.home,name="home"),
    path("privacy/",views.privacy,name="privacy"),
    path("about/",views.about,name="about"),
]

