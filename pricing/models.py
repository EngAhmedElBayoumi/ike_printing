from django.db import models

# Create your models here.

#product discount quantity
class ProductDiscountQuantity(models.Model):
    #minimum quantity
    min_quantity = models.IntegerField()
    #maximum quantity
    max_quantity = models.IntegerField()
    #discount percentage
    discount = models.IntegerField()
    
    #string representation
    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} : {self.price}"
    
    
#printing discount quantity
class PrintingDiscountQuantity(models.Model):
    #minimum quantity
    min_quantity = models.IntegerField()
    #maximum quantity
    max_quantity = models.IntegerField()
    #discount percentage
    discount = models.IntegerField()
    
    #string representation
    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} : {self.price}"


#printing price
class PrintingPrice(models.Model):
    #minimum quantity
    min_size = models.DecimalField(max_digits=5, decimal_places=2)
    #maximum quantity
    max_size = models.DecimalField(max_digits=5, decimal_places=2)
    #price
    price = models.DecimalField(max_digits=5, decimal_places=2)
    #string representation
    def __str__(self):
        return f"{self.min_size} - {self.max_size} : {self.price}"
    
#general discount
class GeneralDiscount(models.Model):
    #name
    discount_name = models.CharField(max_length=50)
    #discount percentage
    discount = models.IntegerField()
    
    #string representation
    def __str__(self):
        return f"{self.discount_name}->{self.discount}"
    
#copoun
class Copoun(models.Model):
    #name
    copoun_name = models.CharField(max_length=50)
    #discount percentage
    discount = models.IntegerField()
    
    #string representation
    def __str__(self):
        return f"{self.copoun_name}->{self.discount}"