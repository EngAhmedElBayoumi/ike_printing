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
            '   <img src="{}" style="max-width: 100px; height: 100px;object-fit: scale-down;" />'
            '   <img src="{}" style="max-width: 100px; height: 100px;object-fit: scale-down;" />'
            '</div>',
            obj.front_tshirt_image,
            obj.back_tshirt_image,
        )
    display_cart_product_images.short_description = 'Images'

    list_display = ('display_cart_product_info', 'display_cart_product_images')
    #search bar
    search_fields = ['product__name','color__name','size__name','matireal__name','quantity','price']

# class OrderResource(resources.ModelResource):
#     user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'username'))
#     total_price = fields.Field(column_name='total_price', attribute='total_price')
#     methods_of_receiving = fields.Field(column_name='methods_of_receiving', attribute='methods_of_receiving')
#     order_date = fields.Field(column_name='order_date', attribute='order_date')

#     cart_product = fields.Field(column_name='cart_product', attribute='cart_product', widget=ManyToManyWidget(CartProduct, 'id'))

#     front_tshirt_image = fields.Field(column_name='front_tshirt_image', attribute=None)
#     back_tshirt_image = fields.Field(column_name='back_tshirt_image', attribute=None)

#     frontcanvas = fields.Field(column_name='frontcanvas', attribute=None)
#     backcanvas = fields.Field(column_name='backcanvas', attribute=None)

#     class Meta:
#         model = Order
#         fields = ('id', 'user', 'cart_product', 'total_price', 'methods_of_receiving', 'order_date', 'front_tshirt_image', 'back_tshirt_image', 'frontcanvas', 'backcanvas')
#         export_order = ('id', 'user', 'cart_product', 'total_price', 'methods_of_receiving', 'order_date', 'front_tshirt_image', 'back_tshirt_image', 'frontcanvas', 'backcanvas')

#     def dehydrate_cart_product(self, order):
#         return ', '.join([f"{cp.product.name} ({cp.quantity})" for cp in order.cart_product.all()])

#     def dehydrate_user(self, order):
#         return order.user.username

#     def dehydrate_order_date(self, order):
#         return order.order_date.strftime('%Y-%m-%d %H:%M:%S')

#     def dehydrate_front_tshirt_image(self, order):
#         return ', '.join([str(cp.front_tshirt_image) for cp in order.cart_product.all()])

#     def dehydrate_back_tshirt_image(self, order):
#         return ', '.join([str(cp.back_tshirt_image) for cp in order.cart_product.all()])

#     def dehydrate_frontcanvas(self, order):
#         return ', '.join([str(cp.frontcanvas) for cp in order.cart_product.all()])

#     def dehydrate_backcanvas(self, order):
#         return ', '.join([str(cp.backcanvas) for cp in order.cart_product.all()])

#     def export_selected_html(modeladmin, request, queryset):
#         html_content = "<html><body>"

#         for order in queryset:
#             html_content += f"<h2>Order #{order.pk}</h2>"
#             html_content += f"<p><strong>User:</strong> {order.user.username}</p>"
#             html_content += f"<p><strong>Total Price:</strong> {order.total_price}</p>"

#             for cart_product in order.cart_product.all():
#                 html_content += f"<h3>Product: {cart_product.product.name}</h3>"
#                 html_content += f"<p><strong>Front T-Shirt Image:</strong> <img src='{cart_product.front_tshirt_image}' style='max-width: 100px; max-height: 100px;'></p>"
#                 html_content += f"<p><strong>Back T-Shirt Image:</strong> <img src='{cart_product.back_tshirt_image}' style='max-width: 100px; max-height: 100px;'></p>"
#                 html_content += f"<p><strong>Front Canvas:</strong> <img src='{cart_product.frontcanvas}' style='max-width: 100px; max-height: 100px;'></p>"
#                 html_content += f"<p><strong>Back Canvas:</strong> <img src='{cart_product.backcanvas}' style='max-width: 100px; max-height: 100px;'></p>"
#                 html_content += f"<p><strong>Quantity:</strong> {cart_product.quantity}</p>"
#                 html_content += f"<p><strong>Price:</strong> {cart_product.total_price}</p>"

#             html_content += "<hr>"

#         html_content += "</body></html>"

#         response = HttpResponse(content_type="text/html")
#         response["Content-Disposition"] = 'attachment; filename="selected_orders.html"'
#         response.write(html_content)

#         return response

#     def embed_image_base64(image_data, max_width=100, max_height=100):
#         return f"<img src='data:image/png;base64,{image_data}' style='max-width: {max_width}px; max-height: {max_height}px;'>"

#     def export_selected_pdf(modeladmin, request, queryset):
#         html_content = "<html><body>"

#         for order in queryset:
#             html_content += f"<h2>Order #{order.pk}</h2>"
#             html_content += f"<p><strong>User:</strong> {order.user.username}</p>"
#             html_content += f"<p><strong>Total Price:</strong> {order.total_price}</p>"

#             for cart_product in order.cart_product.all():
#                 html_content += f"<h3>Product: {cart_product.product.name}</h3>"
#                 html_content += f"<p><strong>Front T-Shirt Image:</strong> {embed_image_base64(cart_product.front_tshirt_image.read())}</p>"
#                 html_content += f"<p><strong>Back T-Shirt Image:</strong> {embed_image_base64(cart_product.back_tshirt_image.read())}</p>"
#                 html_content += f"<p><strong>Front Canvas:</strong> {embed_image_base64(cart_product.frontcanvas)}</p>"
#                 html_content += f"<p><strong>Back Canvas:</strong> {embed_image_base64(cart_product.backcanvas)}</p>"
#                 html_content += f"<p><strong>Quantity:</strong> {cart_product.quantity}</p>"
#                 html_content += f"<p><strong>Price:</strong> {cart_product.total_price}</p>"

#             html_content += "<hr>"

#         html_content += "</body></html>"

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = 'attachment; filename="selected_orders.pdf"'

#         buffer = BytesIO()
#         pisa.CreatePDF(html_content, dest=buffer)

#         pdf_content = buffer.getvalue()
#         buffer.close()

#         response.write(pdf_content)

#         return response
#     export_selected_html.short_description = "Export selected orders to HTML"
#     export_selected_pdf.short_description = "Export selected orders to PDF"



class OrderAdmin(admin.ModelAdmin):
    # resource_class = OrderResource
    list_display = ('display_order_number','display_user_details', 'display_cart_products','display_product_image','display_product_designs' ,'methods_of_receiving', 'total_price', 'order_date')

    def display_order_number(self, obj):
        return f'#{obj.pk}'
    display_order_number.short_description = 'Order Number'
    
    def display_user_details(self, obj):
        return format_html(
            '<strong>Username:</strong> {}<br>'
            '<strong>First Name:</strong> {}<br>'
            '<strong>Last Name:</strong> {}<br>'
            '<strong>Phone:</strong> {}<br>'
            '<strong>Email:</strong> {}<br>'
            '<strong>Address :</strong> {}<br>'
            '<strong>Cuntry and state:</strong> {}<br>'
            '<strong>Postal code:</strong> {}<br>'
            ,
            
            obj.user.username,
            obj.user.first_name,
            obj.user.last_name,
            obj.user.profile.phone,
            obj.user.email,
            obj.user.profile.address,
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
                f'<img src="{cart_product.front_tshirt_image}" style="max-width: 100px; max-height: 100px;object-fit: scale-down;margin-right:10px; margin-top:20px" />'
                #back
                f'<img src="{cart_product.back_tshirt_image}" style="max-width: 100px; max-height: 100px;object-fit: scale-down; margin-top:20px" />'
                for cart_product in cart_products
            )
        )
        
    def  methods_of_receiving(self, obj):
        return f'{obj.methods_of_receiving}'
        
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
    
    # actions = [OrderResource.export_selected_html]
    
    

    
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

admin.site.register(DesignImage)



