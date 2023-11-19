from django.contrib import admin
from .models import ProductDiscountQuantity , PrintingDiscountQuantity , PrintingPrice , GeneralDiscount , Copoun
# Register your models here.

#display product discount quantity
class ProductDiscountQuantityAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('min_quantity','max_quantity','discount')
    #search bar
    search_fields = ['min_quantity']
    
#display printing discount quantity
class PrintingDiscountQuantityAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('min_quantity','max_quantity','discount')
    #search bar
    search_fields = ['min_quantity']
    
#display printing price
class PrintingPriceAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('min_size','max_size','price')
    #search bar
    search_fields = ['min_size']
    
#display general discount
class GeneralDiscountAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('discount_name','discount')
    #search bar
    search_fields = ['discount_name']
    
#display copoun
class CopounAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('copoun_name','discount')
    #search bar
    search_fields = ['copoun_name']
    
#register product discount quantity
admin.site.register(ProductDiscountQuantity,ProductDiscountQuantityAdmin)

#register printing discount quantity
admin.site.register(PrintingDiscountQuantity,PrintingDiscountQuantityAdmin)

#register printing price
admin.site.register(PrintingPrice,PrintingPriceAdmin)

#register general discount
admin.site.register(GeneralDiscount,GeneralDiscountAdmin)

#register copoun
admin.site.register(Copoun,CopounAdmin)




