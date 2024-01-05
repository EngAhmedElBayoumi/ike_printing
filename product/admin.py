from django.contrib import admin
from django.utils.html import format_html

#from .models import Product , matireal , category 
from .models import Product , Matireal , Category , Color , Size , ProductDesign , UserImage , ClipArt , FavoriteProduct ,CartProduct, Order,DesignImage
#import django import export
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import Widget
from import_export import fields, resources
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PIL import Image
import io
from django.http import HttpResponse
#import datetime
from datetime import datetime
from django.utils import timezone
#import strftime
from time import strftime



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


class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    # Display name, description, and other fields
    def display_product_info(self, obj):
        if not obj.is_active:
            # If the product is not active, set the background color to dark
            return format_html(
                '<div style="background-color: #333; padding: 10px; border-radius: 5px;">'
                '   <strong>Name:</strong> {}<br>'
                '   <strong>Description:</strong> {}<br>'
                '   <strong>Height:</strong> {}<br>'
                '   <strong>Category:</strong> {}<br>'
                '   <strong>Colors:</strong> {}<br>'
                '   <strong>Sizes:</strong> {}<br>'
                '   <strong>Materials:</strong> {}<br>'
                '   <strong>Is Active:</strong> {}<br>'
                '</div>',
                obj.name,
                obj.description,
                obj.height,
                obj.category,
                ', '.join(str(color) for color in obj.colors.all()),
                ', '.join(str(size) for size in obj.sizes.all()),
                ', '.join(str(matireal) for matireal in obj.matireal.all()),
                obj.is_active,
            )
        else:
            # If the product is active, no special styling
            return format_html(
                '<strong>Name:</strong> {}<br>'
                '<strong>Description:</strong> {}<br>'
                '<strong>Height:</strong> {}<br>'
                '<strong>Category:</strong> {}<br>'
                '<strong>Colors:</strong> {}<br>'
                '<strong>Sizes:</strong> {}<br>'
                '<strong>Materials:</strong> {}<br>'
                '<strong>Is Active:</strong> {}<br>',
                obj.name,
                obj.description,
                obj.height,
                obj.category,
                ', '.join(str(color) for color in obj.colors.all()),
                ', '.join(str(size) for size in obj.sizes.all()),
                ', '.join(str(matireal) for matireal in obj.matireal.all()),
                obj.is_active,
            )
    display_product_info.short_description = 'Product Info'
    #action deactive product selected
    def deactive_product(self, request, queryset):
        queryset.update(is_active=False)
    deactive_product.short_description = 'Deactive Product'
    #action active product selected
    def active_product(self, request, queryset):
        queryset.update(is_active=True)
    active_product.short_description = 'Active Product'
    
    actions = [deactive_product,active_product]

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
    list_display = ('id','name','display_image')
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


class CartProductResource(resources.ModelResource):
    class Meta:
        model = CartProduct
        fields = ('id', 'user', 'product', 'quantity', 'front_design_price', 'back_design_price', 'quantity_price', 'total_price', 'frontcanvas', 'backcanvas', 'product_color', 'sizes', 'front_tshirt_image', 'back_tshirt_image')
        export_order = ('id', 'user', 'product', 'quantity', 'front_design_price', 'back_design_price', 'quantity_price', 'total_price', 'frontcanvas', 'backcanvas', 'product_color', 'sizes', 'front_tshirt_image', 'back_tshirt_image')

    def dehydrate_user(self, cart_product):
        return cart_product.user.username

    def dehydrate_front_tshirt_image(self, cart_product):
        return self.get_image_data(cart_product.front_tshirt_image)

    def dehydrate_back_tshirt_image(self, cart_product):
        return self.get_image_data(cart_product.back_tshirt_image)

    def get_image_data(self, image_field):
        if image_field:
            image_path = image_field.path
            with open(image_path, 'rb') as image_file:
                return ContentFile(image_file.read(), name=image_field.name)



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
            '   <a href="{}" download><img src="{}" style="max-width: 100px; height: 100px; object-fit: scale-down;" /></a>'
            '   <a href="{}" download><img src="{}" style="max-width: 100px; height: 100px; object-fit: scale-down;" /></a>'
            '</div>',
            obj.front_tshirt_image,  # Assume that front_tshirt_image is an ImageField
            obj.front_tshirt_image,
            obj.back_tshirt_image,   # Assume that back_tshirt_image is an ImageField
            obj.back_tshirt_image,
        )
    
    def display_design_images(self, obj):
        images_html = ''
        for design_image in obj.design_images.all():
            images_html += '<a href="{}" download><img src="{}" width="50" height="50" /></a>'.format(
                design_image.image, design_image.image
            )

        return format_html(images_html)
    
    
    
    display_cart_product_images.short_description = 'Images'

    list_display = ('display_cart_product_info', 'display_cart_product_images','display_design_images')
    #search bar
    search_fields = ['product__name','color__name','size__name','matireal__name','quantity','price']




class OrderAdmin(admin.ModelAdmin):
    # resource_class = OrderResource
    list_display = ('display_order_number','display_user_details', 'display_cart_products','display_product_image','methods_of_receiving', 'total_price', 'order_date','display_order_receiving_date' ,'status', 'display_design_images')

    def display_order_number(self, obj):
        return f'#{obj.pk+1000}'
    
    def display_user_details(self, obj):
        return format_html(
            '<strong>Username:</strong> {}<br>'
            '<strong>First Name:</strong> {}<br>'
            '<strong>Last Name:</strong> {}<br>'
            '<strong>Phone:</strong> {}<br>'
            '<strong>Email:</strong> {}<br>'
            '<strong>Address :</strong> {}<br>'
            '<strong>Address line 2 :</strong> {}<br>'
            '<strong>City and state:</strong> {}<br>'
            '<strong>Postal code:</strong> {}<br>'
            ,
            
            obj.user.username,
            obj.user.first_name,
            obj.user.last_name,
            obj.user.profile.phone,
            obj.user.email,
            obj.user.profile.address,
            obj.user.profile.address_line2,
            obj.user.profile.city + ', ' + obj.user.profile.state ,
            obj.user.profile.postal_code,
        )

    def display_cart_products(self, obj):
        # Display all details in each cart product
        cart_products = obj.cart_product.all()
        #get from Color table name of color
        #color = Color.objects.get(name=cart_products.product_color)
        
        
        return format_html(
            '<br>'.join(
                f'<strong>Product:</strong> {cart_product.product.name}<br>'
                f'<strong>Color:</strong>   <span style="background:{cart_product.product_color};width:20px;height:20px;">{self.get_color_name(cart_product.product_color)}</span><br>'
                #size info symbol and quantity
                f'<strong>Sizes:</strong> {", ".join(f"{size.symbol} ({size.quantity})" for size in cart_product.sizes.all())}<br>'
                f'<strong>Quantity:</strong> {cart_product.quantity}<br>'
                f'<strong>Price:</strong> {cart_product.total_price}<br>'
                for cart_product in cart_products
            )
        )
    def get_color_name(self, color_code):
        try:
            color = Color.objects.get(code=color_code)
            return color.name
        except:
            return color_code            

    def display_product_image(self, obj):
        # Display all details in each cart product
        cart_products = obj.cart_product.all()
        return format_html(
            '<br>'.join(
                #front
                f'<a href="{cart_product.front_tshirt_image}" target="_blank"><img src="{cart_product.front_tshirt_image}" style="max-width: 100px; max-height: 100px;object-fit: scale-down;margin-right:10px; margin-top:20px" /></a>'
                #back
                f'<a href="{cart_product.back_tshirt_image}" target="_blank"><img src="{cart_product.back_tshirt_image}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-top:20px" /></a>'
                for cart_product in cart_products
            )
        )
    
    def  methods_of_receiving(self, obj):
        return f'{obj.methods_of_receiving}'
        
    # def display_product_designs(self, obj):
    #     # Display all details in each cart product
    #     cart_products = obj.cart_product.all()
    #     return format_html(
    #         '<br>'.join(
    #             #front
    #             f'<img src="{cart_product.frontcanvas}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-right:10px; margin-top:40px" />'
    #             #back
    #             f'<img src="{cart_product.backcanvas}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-top:40px" />'
    #             for cart_product in cart_products
    #         )
    #     )
    

    
    
    def display_order_receiving_date(self, obj):
        #date with formate month/day/year
        date = obj.order_receiving_date.strftime("%B/%d/%Y")
        return f'{date}'
    
    def display_design_images(self, obj):
        # loop through all designs images for each cart product on the order and display them in img tags in a tag with download link
        images_html = ''
        for cart_product in obj.cart_product.all():
            for design_image in cart_product.design_images.all():
                images_html += '<a href="{}" download><img src="{}" width="50" height="50" /></a>'.format(
                    design_image.image, design_image.image
                )
                
        return format_html(images_html)
    
    display_order_number.short_description = 'Order Number'
    display_user_details.short_description = 'User Details'
    display_cart_products.short_description = 'Cart Products'
    display_product_image.short_description = 'Product Image'
    # display_product_designs.short_description = 'Product Designs'
    display_design_images.short_description = 'Design Images'
    methods_of_receiving.short_description = 'Methods Of Receiving'
    display_order_receiving_date.short_description = 'Delivery Date'

    
     






class DesignImageAdmin(admin.ModelAdmin):
    #display name , image
    list_display = ('id','display_image')
    #search bar
    search_fields = ['name']
    #display image
    def display_image(self, obj):
        return format_html('<a href="{}" download><img src="{}" width="50" height="50" /></a>', obj.image, obj.image)
    
    display_image.short_description = 'image'



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

admin.site.register(DesignImage,DesignImageAdmin)



