#import path , views 
from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("",views.product,name="product"),
    #product_with_category
    path("product_with_category/<int:category_id>",views.product_with_category,name="product_with_category"),
    path("self_customization/",views.self_customization,name="self_customization"),
    path("self_customization_product/<int:id>",views.self_customization_product,name="self_customization_product"),
    path("ordaring/",views.ordaring,name="ordaring"),
    #getproductsbycategory
    path("getproductsbycategory/<str:category_name>",views.getproductsbycategory,name="getproductsbycategory"),
    #getproductsbycolor
    path("getproductsbycolor/<str:color_name>",views.getproductsbycolor,name="getproductsbycolor"),
    #getproductsbysize
    path("getproductsbysize/<str:size_name>",views.getproductsbysize,name="getproductsbysize"),
    #getproductsbymatireal
    path("getproductsbymatireal/<str:matireal_name>",views.getproductsbymatireal,name="getproductsbymatireal"),
    #save_user_image
    path("save_user_image/",views.save_user_image,name="save_user_image"),
    path("getproductbyid/<int:product_id>",views.getproductbyid,name="getproductbyid"),
    path("edit_product_design/<int:product_id>",views.edit_product_design,name="edit_product_design"),
    #save_design
    path("save_design/",views.save_design,name="save_design"),
    #get_quote
    path("get_quote/",views.get_quote,name="get_quote"),   
    #add_to_card
    path("add_to_card/",views.card,name="card"),
    #remove_from_card by id
    path("remove_from_card/<int:id>",views.remove_from_card,name="remove_from_card"),
    #clear card
    path("clear_card/",views.clear_card,name="clear_card"),
    #apply_copoun
    path("apply_copoun/",views.apply_copoun,name="apply_copoun"),
    #order
    path("order/",views.order,name="order"),
    #payment success
    path("payment_success/",views.payment_success,name="payment_success"),
    #payment failed
    path("payment_failed/",views.payment_failed,name="payment_failed"),
    
    path("order_page/",views.order_page,name="order_page"),
    
]
