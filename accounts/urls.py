#import path , views
from django.urls import path

from . import views

app_name = "accounts"
 
urlpatterns = [
    #login
    path("login/",views.log_in,name="login"),
    #logout
    path("logout/",views.log_out,name="logout"),
    #register
    path("register/",views.register,name="register"),
    #profile
    path("profile/",views.profile,name="profile"),
    #forgot_password
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    #reset_password
    path("reset_password/",views.reset_password,name="reset_password"),
    #my_orders
    path("my_orders/",views.my_orders,name="my_orders"),
    #my_images
    path("my_images/",views.my_images,name="my_images"),
    #my_designs
    path("my_designs/",views.my_designs,name="my_designs"),
    #wishlist
    path("wishlist/",views.wishlist,name="wishlist"),
    #addresses
    path("addresses/",views.addresses,name="addresses"),
    #payment_methods
    path("payment_methods/",views.payment_methods,name="payment_methods"),
    
]