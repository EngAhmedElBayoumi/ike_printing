#import path 
from django.urls import path
#import views from pricing app
from . import views

#app name
app_name = 'pricing'

#url patterns
urlpatterns = [
    path('calculate_price/', views.calculate_price, name='calculate_price')
]

