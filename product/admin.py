from django.contrib import admin
from django.utils.html import format_html

#from .models import Product , matireal , category 
from .models import Product , Matireal , Category , Color , Size , ProductDesign , UserImage , ClipArt , FavoriteProduct ,CartProduct

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','display_image', 'price', 'category', 'display_matireals')
    list_filter = ('category',)
    
    def display_matireals(self, obj):
        matireals_info = [f"{matireal.name} : {matireal.percentage}%" for matireal in obj.matireal.all()]
        return ", ".join(matireals_info)

    display_matireals.short_description = 'Matireals'
    
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.frontimage.url)
    
    display_image.short_description = 'frontimage'

# Register the model with the custom admin class



#search bar
class MatirealAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','percentage')
            
    
#clip art display
class ClipArtAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('name','display_image')
    #search bar
    search_fields = ['name']
    #display image
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
    
    display_image.short_description = 'image'
    
    
    
#category display
class CategoryAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('name','display_image')
    #search bar
    search_fields = ['name']
    #display image
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
    
    display_image.short_description = 'image'
    
        
#color display
class ColorAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('name','code')
    #search bar
    search_fields = ['name']
    
        
# size display
class SizeAdmin(admin.ModelAdmin):
    # display name , image
    list_display = ('name', 'simbol', 'display_height', 'display_width', 'display_price')
    # search bar
    search_fields = ['name']

    def display_height(self, obj):
        return f'{obj.height} in'

    display_height.short_description = 'Height'

    def display_width(self, obj):
        return f'{obj.width} in'

    display_width.short_description = 'Width'

    def display_price(self, obj):
        return f'${obj.price}'

    display_price.short_description = 'Price'

    

#product design display
class ProductDesignAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('name','display_image')
    #search bar
    search_fields = ['name']
    #display image
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.frontimage.url)
    
    display_image.short_description = 'image'


#user image display
class UserImageAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('user','display_image')
    #search bar
    search_fields = ['user']
    #display image
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
    
    display_image.short_description = 'image'





admin.site.register(Product, ProductAdmin)
admin.site.register(Matireal,MatirealAdmin)
admin.site.register(ClipArt,ClipArtAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(ProductDesign,ProductDesignAdmin)
admin.site.register(UserImage,UserImageAdmin)
admin.site.register(CartProduct)





