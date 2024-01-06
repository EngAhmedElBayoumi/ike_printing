from django.db import models
import json
#import user
from django.contrib.auth.models import User
import requests
import base64
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.files.temp import NamedTemporaryFile
from django.utils.html import format_html


# Create your models here.

#category , product , matireal models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='product/category_image')

    def __str__(self):
        return self.name
    
    
class Color(models.Model):
    #color code
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=50)
    #simbol
    simbol = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"

  
  
class Matireal(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='product/matireal_image',blank=True,null=True)
    percentage =models.IntegerField()
    def __str__(self):
        return self.name 
    
  

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    height = models.CharField(max_length=50)
    frontimage = models.ImageField(upload_to='product/product_image')
    backimage = models.ImageField(upload_to='product/product_image')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    colors = models.ManyToManyField(Color)
    sizes = models.ManyToManyField(Size)
    matireal=models.ManyToManyField(Matireal)
    #deactive product
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    
 
    
    
#clip art
class ClipArt(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product/clipart_image')
    def __str__(self):
        return self.name
    
#userimage
class UserImage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product/userimage_image')
    def __str__(self):
        return self.name
    

#product design user relation , product relation , front canvas , back canvas , sizeing 

class ProductDesign(models.Model):
    user = models.ManyToManyField(User)
    name=models.CharField(max_length=50)
    frontcanvas = models.TextField()
    backcanvas = models.TextField()
    frontimage=models.ImageField(upload_to='product/productdesign_image',blank=True,null=True)
    def __str__(self):
        return self.name
    
    #get front canvas data
    def get_frontcanvas(self):
        return json.loads(self.frontcanvas)
    
    #get back canvas data
    def get_backcanvas(self):
        return json.loads(self.backcanvas)
    
    #set front canvas data
    def set_frontcanvas(self):
        self.frontcanvas=json.dumps(self.frontcanvas)
        
        
    #set back canvas data
    def set_backcanvas(self):
        self.backcanvas=json.dumps(self.backcanvas)
        
        

#favorite product
class FavoriteProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
    
    
#card_size
class CardSize(models.Model):
    symbol = models.CharField(max_length=50)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.symbol
  
  
#design images resourse
class DesignImage(models.Model):
    #text field for image with method json.dumps and json.loads
    image = models.TextField()

    def __str__(self):
        return str(self.id)
    
    #get image
    def get_image(self):
        return json.loads(self.image)
    
    #set image
    def set_image(self):
        self.image=json.dumps(self.image)
    
        
#cart product
class CartProduct(models.Model):
    user = models.ManyToManyField(User)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    front_design_price = models.FloatField()
    back_design_price = models.FloatField()
    quantity_price = models.FloatField()
    total_price = models.FloatField()
    frontcanvas = models.TextField()
    backcanvas = models.TextField()
    product_color = models.CharField(max_length=50)
    sizes = models.ManyToManyField(CardSize)
    front_tshirt_image = models.ImageField(upload_to='product/cartproduct_image',blank=True,null=True)
    back_tshirt_image = models.ImageField(upload_to='product/cartproduct_image',blank=True,null=True)
    #design images
    design_images = models.ManyToManyField(DesignImage)
    
    def __str__(self):
        return self.product.name
    
    #get front canvas data
    def get_frontcanvas(self):
        return json.loads(self.frontcanvas)
    
    #get back canvas data
    def get_backcanvas(self):
        return json.loads(self.backcanvas)
    
    #set front canvas data
    def set_frontcanvas(self):
        self.frontcanvas=json.dumps(self.frontcanvas)

    #set back canvas data
    def set_backcanvas(self):
        self.backcanvas=json.dumps(self.backcanvas)
   

#order status  Processing/ in Progress/ Ready For Pickup/ Shipping/ Delivered/ Finished
order_status = (
    ('Processing','Processing'),
    ('in_Progress','in_Progress'),
    ('Ready_For_Pickup','Ready_For_Pickup'),
    ('Shipping','Shipping'),
    ('Delivered','Delivered'),
    ('Finished','Finished'),
    )    

 
          
#order
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_product = models.ManyToManyField(CartProduct)
    total_price = models.FloatField()
    #methods of receiving
    methods_of_receiving = models.CharField(max_length=50, default="pickup")
    order_date = models.DateTimeField(auto_now_add=True)
    #order receiving date not time
    order_receiving_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=50,default="Processing",choices=order_status)
    def __str__(self):
        return self.user.username
    
    


        
    

    

    

