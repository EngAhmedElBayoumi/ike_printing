from django.contrib import admin
from django.utils.html import format_html

#from .models import Product , matireal , category 
from .models import Product , Matireal , Category , Color , Size , ProductDesign , UserImage , ClipArt , FavoriteProduct ,CartProduct, Order
#import django import export
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import Widget


# Register your models here.

class ImageWidget(Widget):
    """
    Custom Widget to display images in export.
    """

    def render(self, value, obj=None):
        return format_html('<img src="{}" width="50" height="50" />', value)


class ProductResource(resources.ModelResource):
    frontimage = fields.Field(column_name='Front Image', attribute='get_frontimage_url')
    backimage = fields.Field(column_name='Back Image', attribute='get_backimage_url')

    def get_frontimage_url(self, product):
        return product.frontimage.url

    def get_backimage_url(self, product):
        return product.backimage.url

    class Meta:
        model = Product
        fields = ('name', 'description', 'height', 'category', 'colors', 'sizes', 'matireal', 'frontimage', 'backimage')
        export_order = ('name', 'description', 'height', 'category', 'colors', 'sizes', 'matireal', 'frontimage', 'backimage')



class ProductAdmin(admin.ModelAdmin):
    # Display name, description, and other fields
    def display_product_info(self, obj):
        return format_html(
            '<strong>Name:</strong> {}<br>'
            '<strong>Description:</strong> {}<br>'
            '<strong>Height:</strong> {}<br>'
            '<strong>Category:</strong> {}<br>'
            '<strong>Colors:</strong> {}<br>'
            '<strong>Sizes:</strong> {}<br>'
            '<strong>Matireals:</strong> {}<br>',
            obj.name,
            obj.description,
            obj.height,
            obj.category,
            ', '.join(str(color) for color in obj.colors.all()),
            ', '.join(str(size) for size in obj.sizes.all()),
            ', '.join(str(matireal) for matireal in obj.matireal.all()),
        )
    display_product_info.short_description = 'Product Info'

    # Display front and back images
    def display_product_images(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; justify-content: center;">'
            '   <img src="{}" style="max-width: 100px; max-height: 100px;object-fit: scale-down;" />'
            '   <img src="{}" style="max-width: 100px; max-height: 100p;object-fit: scale-down;" />'
            '</div>',
            obj.frontimage.url,
            obj.backimage.url,
        )
    display_product_images.short_description = 'Images'

    list_display = ('display_product_info', 'display_product_images')
    #search bar
    search_fields = ['name','description','height','category__name','colors__name','sizes__name','matireal__name']
    resource_class = ProductResource  
    

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
    list_display = ('name', 'simbol', 'display_price')
    # search bar
    search_fields = ['name']

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
        return format_html('<img src="{}" style="width:50%; height=50%;" />', obj.frontimage)
    
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

#CartProduct display all fields in admin panel in multiple line
class CartProductAdmin(admin.ModelAdmin):
    # Display name, description, and other fields
    def display_cart_product_info(self, obj):
        size_info = [f"{size.symbol} ({size.quantity})" for size in obj.sizes.all()]
        
        return format_html(
            
            '<strong>User:</strong> {}<br>'
            '<strong>Product:</strong> {}<br>'
            '<strong>Color:</strong> {}<br>'
            '<strong>Sizes:</strong> {}<br>'
            '<strong>Quantity:</strong> {}<br>'
            '<strong>Price:</strong> {}<br>',
            obj.user,
            obj.product,
            obj.product_color,
            ', '.join(size_info),  # Join size info strings with a comma
            obj.quantity,
            obj.total_price,
        )
    display_cart_product_info.short_description = 'Cart Product Info'

    # Display front and back images
    def display_cart_product_images(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; justify-content: center;">'
            '   <img src="{}" style="max-width: 100px; max-height: 100px;object-fit: scale-down;" />'
            '   <img src="{}" style="max-width: 100px; max-height: 100p;object-fit: scale-down;" />'
            '</div>',
            obj.product.frontimage.url,
            obj.product.backimage.url,
        )
    display_cart_product_images.short_description = 'Images'

    list_display = ('display_cart_product_info', 'display_cart_product_images')
    #search bar
    search_fields = ['product__name','color__name','size__name','matireal__name','quantity','price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('display_user_details', 'display_cart_products','display_product_image','display_product_designs' , 'total_price', 'order_date')

    def display_user_details(self, obj):
        return format_html(
            '<strong>Username:</strong> {}<br>'
            '<strong>First Name:</strong> {}<br>'
            '<strong>Last Name:</strong> {}<br>'
            '<strong>Phone:</strong> {}<br>'
            
            '<strong>Email:</strong> {}<br>'
            '<strong>Address:</strong> {}<br>'
            '<strong>Postal code:</strong> {}<br>'
            ,
            
            obj.user.username,
            obj.user.first_name,
            obj.user.last_name,
            obj.user.profile.phone,
            obj.user.email,
            obj.user.profile.country + ', ' + obj.user.profile.state ,
            obj.user.profile.postal_code,
            
            
        )


    def display_cart_products(self, obj):
        # Display all details in each cart product
        cart_products = obj.cart_product.all()
        return format_html(
            '<br>'.join(
                f'<strong>Product:</strong> {cart_product.product.name}<br>'
                f'<strong>Color:</strong>   <span style="background:{cart_product.product_color};width:20px;height:20px;">{cart_product.product_color}</span><br>'
                #size info symbol and quantity
                f'<strong>Sizes:</strong> {", ".join(f"{size.symbol} ({size.quantity})" for size in cart_product.sizes.all())}<br>'
                f'<strong>Quantity:</strong> {cart_product.quantity}<br>'
                f'<strong>Price:</strong> {cart_product.total_price}<br>'
                for cart_product in cart_products
            )
        )
    
    def display_product_image(self, obj):
        # Display all details in each cart product
        cart_products = obj.cart_product.all()
        return format_html(
            '<br>'.join(
                #front
                f'<img src="{cart_product.product.frontimage.url}" style="max-width: 100px; max-height: 100px;object-fit: scale-down;margin-right:10px; margin-top:20px" />'
                #back
                f'<img src="{cart_product.product.backimage.url}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-top:20px" />'
                for cart_product in cart_products
            )
        )
        
    def display_product_designs(self, obj):
        # Display all details in each cart product
        cart_products = obj.cart_product.all()
        return format_html(
            '<br>'.join(
                #front
                f'<img src="{cart_product.frontcanvas}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-right:10px; margin-top:40px" />'
                #back
                f'<img src="{cart_product.backcanvas}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-top:40px" />'
                for cart_product in cart_products
            )
        )
    display_user_details.short_description = 'User Details'
    display_cart_products.short_description = 'Products'
    display_product_image.short_description = 'Product Image'
    display_product_designs.short_description = 'Product Designs'


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Matireal,MatirealAdmin)
admin.site.register(ClipArt,ClipArtAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(ProductDesign,ProductDesignAdmin)
admin.site.register(UserImage,UserImageAdmin)
admin.site.register(CartProduct,CartProductAdmin)





