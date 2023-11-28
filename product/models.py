from django.db import models
import json
#import user
from django.contrib.auth.models import User


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
    def __str__(self):
        return self.name
    
    
 
    
    
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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    frontcanvas = models.TextField()
    backcanvas = models.TextField()
    frontimage=models.ImageField(upload_to='product/productdesign_image',blank=True,null=True)
    def __str__(self):
        return self.user.username
    
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
    
    
#cart product
class CartProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    front_design_price = models.FloatField()
    back_design_price = models.FloatField()
    quantity_price = models.FloatField()
    total_price = models.FloatField()
    frontcanvas = models.TextField()
    backcanvas = models.TextField()
    def __str__(self):
        return self.user.username
    
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
        
            
    
    


        
    

    

    

